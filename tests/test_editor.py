"""Browser and geometry regressions for the self-contained original editor.
Run: python3 -m unittest discover -s tests -v
Requires Playwright and Chromium (CHROMIUM_PATH optionally selects a system build).
These checks validate software behavior, never physical machining safety.
"""
import functools
import hashlib
import http.server
import math
import os
from pathlib import Path
import shutil
import struct
import threading
import unittest

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


class EditorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = http.server.ThreadingHTTPServer(
            ('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT)))
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.playwright = sync_playwright().start()
        executable = os.environ.get('CHROMIUM_PATH') or shutil.which('chromium')
        cls.browser = cls.playwright.chromium.launch(
            executable_path=executable, headless=True, args=['--no-sandbox'])
        cls.url = f'http://127.0.0.1:{cls.server.server_port}/editor-usinagem-indexada.html'

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()
        cls.server.shutdown()
        cls.server.server_close()

    def setUp(self):
        self.page = self.browser.new_page(viewport={'width': 1440, 'height': 1100})
        self.errors = []
        self.page.on('pageerror', lambda error: self.errors.append(str(error)))
        self.page.goto(self.url)
        self.page.wait_for_function('sg.length > 0')

    def tearDown(self):
        self.page.close()
        self.assertEqual(self.errors, [])

    def js(self, expression):
        return self.page.evaluate(expression)

    def test_original_controls_desktop_mobile_and_export(self):
        self.assertEqual(self.page.locator('canvas').count(), 6)
        self.assertIn('G91.1', self.page.locator('#out').input_value())
        self.page.locator('#addR').click()
        self.page.locator('#r45').click()
        self.page.locator('#addL').click()
        self.assertEqual(self.js('ops.length'), 3)
        self.page.locator('#cm').select_option('out')
        self.page.wait_for_timeout(100)
        self.assertIn('Y-1.5', self.page.locator('#out').input_value())
        with self.page.expect_download() as pending:
            self.page.locator('#download').click()
        download = pending.value
        self.assertTrue(download.suggested_filename.endswith('.nc'))
        exported = Path(download.path()).read_text()
        self.assertTrue(exported.endswith('M30\n'))
        self.assertIn('nao homologado', exported)
        self.page.set_viewport_size({'width': 390, 'height': 844})
        self.page.wait_for_timeout(100)
        self.assertTrue(self.js('document.documentElement.scrollWidth <= innerWidth'))
        self.page.screenshot(path='/tmp/makernauta-mobile.png', full_page=True)

    def test_tools_are_independent_in_selection_and_removal(self):
        values = self.js('''() => {
          $('TS').value=6;$('TY').value='1';$('T').value=2;$('HT').value='0';$('T').oninput();
          const q={x:30,y:0,z:9,a:0};
          const sculpture=toolFor({h:0}),pocket=toolFor({h:1});
          return {sculpture,pocket,
            ballEdge:cutterRadiusAt(2,0,q,sculpture),
            flatEdge:cutterRadiusAt(.8,0,q,pocket)};
        }''')
        self.assertEqual(values['sculpture'], {'diameter': 6, 'ball': True})
        self.assertEqual(values['pocket'], {'diameter': 2, 'ball': False})
        self.assertAlmostEqual(values['ballEdge'], 12-math.sqrt(5))
        self.assertAlmostEqual(values['flatEdge'], 9)
        self.assertTrue(self.js("() => {$('TY').value='0';$('HT').value='1';$('HT').oninput();return !toolFor({h:0}).ball&&toolFor({h:1}).ball}"))

    def test_indexed_coordinates_align_for_both_a_directions_and_z_origins(self):
        error = self.js('''() => {
          let error=0;
          for(const dir of [1,-1])for(const origin of ['0','1'])for(const a of [0,45,90,180,270,360]){
            $('DIR').value=dir;$('Z0').value=origin;
            const z=9,y=2,angle=a*Math.PI/180;
            const fixed=indexedPoint(30,y,z,a,1,0);
            error=Math.max(error,Math.abs(fixed[1]-(y*Math.cos(angle)+z*Math.sin(angle))),Math.abs(fixed[2]-(z*Math.cos(angle)-y*Math.sin(angle))));
            const machine=indexedPoint(30,y,z,a,1,angle);
            error=Math.max(error,Math.abs(machine[1]-y),Math.abs(machine[2]-z));
          }return error;
        }''')
        self.assertLess(error, 1e-10)

    def test_flat_floor_ball_profile_and_scrub_reset(self):
        self.js("$('ql').value='0';$('rf').value='0';ops[0].a=90;draw();v3();tt=tot;dr3()")
        result = self.js('''() => {
          const K=PK[0],index=Math.round((30-K.x0)/.15),j=Math.round(-K.y0/.15);
          let min=Infinity, max=-Infinity;
          for(let di=-5;di<=5;di++)for(let dj=-5;dj<=5;dj++){
            const z=K.z[(j+dj)*K.nx+index+di];min=Math.min(min,z);max=Math.max(max,z);
          }
          return {min,max,removed:FLD.filter(r=>r<14.9).length};
        }''')
        self.assertAlmostEqual(result['min'], 9, places=3)
        self.assertAlmostEqual(result['max'], 9, places=3)
        self.assertGreater(result['removed'], 0)
        self.js('tt=0;dr3()')
        self.assertEqual(self.js('FLD.filter(r=>r<15).length'), 0)
        self.js("$('HT').value='1';$('HT').oninput();draw();v3();tt=tot;dr3()")
        self.assertGreater(self.js('Object.values(PK).filter(k=>k.n).length'), 0)
        self.page.screenshot(path='/tmp/makernauta-desktop.png', full_page=True)

    def test_exact_rotary_flat_and_ball_intersections(self):
        for ball in (False, True):
            result = self.page.evaluate('''ball => {
              const q={x:30,y:0,z:9,a:90},tool={diameter:6,ball};
              const phi=(90+5)*Math.PI/180,r=cutterRadiusAt(0,phi,q,tool),delta=5*Math.PI/180;
              return {r,y:r*Math.sin(delta),z:r*Math.cos(delta)};
            }''', ball)
            if ball:
                self.assertAlmostEqual(result['y']**2+(result['z']-12)**2, 9, places=8)
            else:
                self.assertAlmostEqual(result['z'], 9, places=8)

    def test_ballnose_shank_removes_material_above_spherical_tip(self):
        # This off-axis ray misses the sphere and first meets its cylindrical shank.
        radius = self.js("cutterRadiusAt(0,Math.atan(2/20),{x:0,y:5,z:9,a:0},{diameter:6,ball:true})")
        self.assertAlmostEqual(radius, math.hypot(2, 20), places=7)

    def test_material_removal_matches_indexed_path_in_all_references(self):
        result = self.js('''() => {
          const failures=[];$('ql').value='0';$('TS').value=3;$('TY').value='0';
          for(const dir of [1,-1])for(const origin of ['0','1'])for(const angle of [0,90,180,270]){
            $('DIR').value=dir;$('Z0').value=origin;grid();
            const i=Math.round((NXG-1)/2),x=i*P().L/(NXG-1),q={x,y:0,z:9-(+origin?15:0),a:angle*dir};
            carveSeg({p:q,q,r:false,h:0},0,1);
            const j=Math.round(angle/360*NPG)%NPG,at=FLD[i*NPG+j],opposite=FLD[i*NPG+(j+NPG/2)%NPG];
            if(Math.abs(at-9)>1e-6||opposite!==15)failures.push({dir,origin,angle,at,opposite});
          }return failures;
        }''')
        self.assertEqual(result, [])

    def test_aspire_xza_import_phase_tools_and_combined_mach3(self):
        code = '(Aspire XZA)\nG21 G90 G17\nG0 X10 Y0 Z23 A0\nS18000 M3\nG1 X20 Z12 A90 F1000\ng1 x30 z11 a180\nN100 M30\n'
        self.page.locator('#fsc').set_input_files({'name':'aspire.nc','mimeType':'text/plain','buffer':code.encode()})
        self.page.wait_for_function("$('si').textContent.includes('Coordenadas')")
        self.page.locator('#confirmCenter').click()
        self.page.wait_for_timeout(250)
        output = self.page.locator('#out').input_value()
        self.assertIn('FIM DA ESCULTURA', output)
        self.assertIn('M0 (Troque a fresa e confirme)', output)
        self.assertEqual(output.count('M30'), 1)
        self.assertTrue(self.js('sg.some(s=>!s.h&&s.q.a===180)&&sg.some(s=>s.h)'))
        self.assertTrue(self.js('sg.some(s=>!s.h&&toolFor(s).ball)'))
        self.page.locator('#OM').select_option('0')
        self.page.wait_for_timeout(250)
        self.assertNotIn('FIM DA ESCULTURA', self.page.locator('#out').input_value())
        self.page.locator('#simStage').select_option('pockets')
        self.assertTrue(self.js('sg.every(s=>s.h)'))

    def test_ascii_and_binary_stl_import_rotation_and_surface_floor(self):
        before=self.page.locator('#out').input_value()
        vertices=[(0,-5,-5),(0,5,-5),(0,5,5),(0,-5,5),(40,-5,-5),(40,5,-5),(40,5,5),(40,-5,5)]
        faces=[(0,1,2),(0,2,3),(4,6,5),(4,7,6),(0,4,5),(0,5,1),(3,2,6),(3,6,7),(0,3,7),(0,7,4),(1,5,6),(1,6,2)]
        ascii_stl='solid target\n'+''.join('facet normal 0 0 0\nouter loop\n'+''.join('vertex %s %s %s\n'%vertices[i] for i in face)+'endloop\nendfacet\n' for face in faces)+'endsolid target'
        binary=bytearray(80)+struct.pack('<I',len(faces))
        for face in faces:
            binary+=struct.pack('<12fH',0,0,0,*(v for i in face for v in vertices[i]),0)
        for name,data in [('ascii.stl',ascii_stl.encode()),('binary.stl',bytes(binary))]:
            self.page.locator('#fst').set_input_files({'name':name,'mimeType':'model/stl','buffer':data})
            self.page.wait_for_function("$('sti').textContent.startsWith('STL lido:')")
            self.assertTrue(self.js('FLD.every(r=>r===P().D/2)'))
            self.assertEqual(self.page.locator('#out').input_value(),before)
            self.assertEqual(self.js('tt'),0)
            self.assertEqual(self.js('TRI.length/9'),12)
            self.assertEqual(self.js('TLEN'),40)
            self.assertGreater(self.js('Math.max(...TGT)'),5)
        self.page.locator('#fit').click()
        self.assertEqual(self.page.locator('#L').input_value(),'40')
        self.page.locator('#SR').fill('90')
        self.page.locator('#SR').dispatch_event('change')
        self.page.locator('#SX').check()
        self.page.wait_for_timeout(100)
        self.assertEqual(self.page.locator('#SR').input_value(),'90')
        self.assertTrue(self.page.locator('#SX').is_checked())

    def test_rendered_line_groove_retains_ballnose_curvature(self):
        # Measure the detailed Cartesian section; the 3D surface uses the radial field.
        result = self.js('''() => {
          ops.splice(0,ops.length,{t:'r',ln:true,cm:'on',x:30,a:0,w:6,l:20,d:4});sel=0;
          ops[0].toolDiameter=6;$('T').value=6;$('SD').value=4;$('ql').value='0';
          const results={};
          for(const type of ['0','1']){
            ops[0].toolType=type;$('HT').value=type;draw();v3();tt=tot;dr3();
            const K=PK[0];results[type]=[0,.75,1.5,2.25].map(y=>pocketSample(K,30,y,ops[0]));
          }
          return results;
        }''')
        for height in result['0']:
            self.assertAlmostEqual(height, 11, delta=.001)
        for y, height in zip([0,.75,1.5,2.25], result['1']):
            self.assertAlmostEqual(height, 14-math.sqrt(9-y*y), delta=.02)
        self.assertGreater(result['1'][-1]-result['1'][0], .9)
        self.assertIn('Ballnose', self.page.locator('#cutStatus').text_content())
        self.page.locator('#cutProfile').screenshot(path='/tmp/makernauta-ballnose-profile.png')
        self.page.locator('#c3').screenshot(path='/tmp/makernauta-ballnose-3d.png')

    def test_pocket_sculpture_baseline_is_not_overwritten_between_layers(self):
        result = self.js('''() => {
          $('ql').value='0';$('HT').value='1';draw();v3();
          tt=tot;dr3();const first=Array.from(BS);
          return {baselineUncut:first.every(r=>r===15),changed:FLD.some(r=>r<15)};
        }''')
        self.assertTrue(result['baselineUncut'])
        self.assertTrue(result['changed'])

    def test_information_covers_all_controls_and_preserves_checkbox_values(self):
        self.page.locator('#helpToggle').click()
        self.assertEqual(self.page.locator('#helpToggle').get_attribute('aria-pressed'),'true')
        missing=self.js('''[...document.querySelectorAll('input[id],select[id],textarea[id],button[id]')].filter(e=>e.id!=='helpToggle'&&!parameterHelp[e.id]).map(e=>e.id)''')
        self.assertEqual(missing, [])
        self.page.locator('[data-help-for="HT"]').click()
        self.assertTrue(self.page.locator('#paramHelp').is_visible())
        self.assertIn('ponta hemisférica', self.page.locator('#helpBody').text_content())
        self.page.keyboard.press('Escape')
        before=self.page.locator('#ST').is_checked()
        self.page.locator('[data-help-for="ST"]').click()
        self.assertEqual(self.page.locator('#ST').is_checked(),before)
        self.page.get_by_role('button',name='Fechar',exact=True).click()
        self.page.locator('[data-help-for="vm"]').click()
        self.assertIn('não o resultado da fresa',self.page.locator('#helpBody').text_content())
        self.page.keyboard.press('Escape')
        self.page.set_viewport_size({'width':390,'height':844})
        self.assertTrue(self.js('document.documentElement.scrollWidth<=innerWidth'))
        self.page.locator('#helpToggle').click()
        self.assertEqual(self.page.locator('.param-info:visible').count(),0)

    def test_each_figure_keeps_its_tool_and_exports_tool_changes(self):
        self.page.locator('#T').fill('6')
        self.page.locator('#HT').select_option('1')
        self.page.locator('#addR').click()
        self.assertEqual(self.page.locator('#T').input_value(),'3')
        self.page.locator('#T').fill('4')
        self.page.locator('#addL').click()
        self.page.locator('#T').fill('2')
        self.page.locator('#list button').nth(0).click()
        self.assertEqual(self.page.locator('#T').input_value(),'6')
        self.assertEqual(self.page.locator('#HT').input_value(),'1')
        self.page.wait_for_timeout(100)
        text=self.page.locator('#out').input_value()
        self.assertIn('Ferramenta alojamento 1: ballnose D6',text)
        self.assertIn('Ferramenta alojamento 2: topo reto D4',text)
        self.assertIn('Ferramenta alojamento 3: topo reto D2',text)
        self.assertEqual(text.count('M0 (Troque a fresa para o proximo alojamento'),2)
        self.assertTrue(self.js("sg.some(g=>g.h&&g.o===0&&toolFor(g).diameter===6&&toolFor(g).ball)&&sg.some(g=>g.h&&g.o===1&&toolFor(g).diameter===4&&!toolFor(g).ball)&&sg.some(g=>g.h&&g.o===2&&toolFor(g).diameter===2)"))
        self.js('tt=tot;dr3()')
        self.assertEqual(self.js('Object.keys(PK).length'),3)
        self.page.locator('#list button').nth(1).click()
        self.assertEqual(self.page.locator('#T').input_value(),'4')
        self.assertEqual(self.page.locator('#HT').input_value(),'0')

    def test_parameters_are_in_their_functional_sections(self):
        for section,ids in {'pocketSection':['T','HT','ST'],'machineSection':['D','L','S','F','FP','SD','SF','DIR','Z0'],'aspireSection':['TS','TY','sc','fsc','confirmCenter','confirmSurface'],'stlSection':['fst','fit','SR','SX','vm']}.items():
            for control in ids:
                self.assertEqual(self.page.locator(f'#{section} #{control}').count(),1)
        self.assertEqual(self.page.locator('#aspireSection #Z0').count(),0)
        self.assertFalse(self.page.locator('#ST').is_checked())

    def test_unknown_aspire_origin_blocks_export_until_confirmed_and_mismatch_blocks(self):
        code='G21 G90 G17\nG0 X10 Z23 A0\nG1 X20 Z12 A90 F1000\nM30'
        self.page.locator('#sc').fill(code)
        self.assertEqual(self.page.locator('#out').input_value(),'')
        self.assertTrue(self.page.locator('#download').is_disabled())
        self.assertIn('Confirme',self.page.locator('#err').text_content())
        self.assertEqual(self.page.locator('#Z0').input_value(),'0')
        self.page.locator('#confirmSurface').click()
        self.assertIn('incompatível',self.page.locator('#err').text_content())
        self.assertEqual(self.page.locator('#out').input_value(),'')
        self.page.locator('#Z0').select_option('1')
        self.assertIn('G1 X20 Z12 A90 F1000',self.page.locator('#out').input_value())
        self.assertEqual(self.page.locator('#sc').input_value(),code)
        self.page.locator('#sc').fill(code+'\n(comment edit)')
        self.assertEqual(self.page.locator('#out').input_value(),'')
        self.assertIsNone(self.js('sourceReference()'))

    def test_explicit_aspire_reference_preserves_xyz_a_and_uses_phase_offset(self):
        code='(Z0 = superficie do bruto)\nG21 G90 G17\nG0 X10 Y0 Z8 A0\nG1 X20 Z-3 A90 F1000\nM30'
        self.page.locator('#sc').fill(code)
        self.assertEqual(self.js('sourceReference()'),'1')
        self.assertTrue(self.page.locator('#confirmCenter').is_disabled())
        self.assertEqual(self.page.locator('#Z0').input_value(),'0')
        self.page.locator('#simStage').select_option('sculpture')
        self.page.wait_for_timeout(100)
        original=self.js('sg.filter(g=>!g.r).map(g=>({x:g.q.x,z:g.q.z,a:g.q.a,zo:g.q.zo}))')
        self.assertEqual(original,[{'x':20,'z':-3,'a':90,'zo':15}])
        self.page.locator('#DIR').select_option('-1')
        self.page.locator('#Z0').select_option('1')
        self.page.wait_for_timeout(100)
        self.assertEqual(self.js('sg.filter(g=>!g.r).map(g=>({x:g.q.x,z:g.q.z,a:g.q.a,zo:g.q.zo}))'),original)
        self.page.locator('#simStage').select_option('all')
        self.assertIn('G1 X20 Z-3 A90 F1000',self.page.locator('#out').input_value())
        self.assertTrue(self.js('sg.every(g=>g.q.ad===-1)'))

    def test_combined_export_requires_tool_change_and_does_not_rewrite_modes(self):
        self.page.locator('#sc').fill('(Z0 = centro)\nG21 G90 G17\nG0 Z23\nG1 X20 Z12 A90 F1000\nN100 M30')
        self.page.locator('#PZ').uncheck()
        self.assertEqual(self.page.locator('#out').input_value(),'')
        self.assertIn('pausa',self.page.locator('#err').text_content())
        self.page.locator('#PZ').check()
        self.assertIn('G1 X20 Z12 A90 F1000',self.page.locator('#out').input_value())
        self.page.locator('#sc').fill('(Z0 = centro)\nG21 G91\nG1 X20 Z12 A90 F1000')
        self.assertEqual(self.page.locator('#out').input_value(),'')
        self.assertIn('não suportados',self.page.locator('#err').text_content())

    def test_ambiguous_comments_require_confirmation_and_modes_are_not_converted(self):
        self.page.locator('#sc').fill('(Z0 = centro ou superficie)\nG21 G90\nG1 X20 Z10 A90')
        self.assertIsNone(self.js('sourceReference()'))
        self.assertEqual(self.page.locator('#out').input_value(),'')
        self.page.locator('#confirmCenter').click()
        self.assertIn('G1 X20 Z10 A90',self.page.locator('#out').input_value())
        self.page.locator('#sc').fill('(Z0 = centro)\nG20 G90\nG1 X20 Z10 A90')
        self.assertEqual(self.page.locator('#out').input_value(),'')
        self.assertIn('G20',self.page.locator('#sc').input_value())

    def test_simulation_stage_and_reference_view_are_distinct(self):
        self.page.locator('#sc').fill('(Z0 = centro)\nG21 G90 G17\nG0 X10 Z23 A0\nG1 X20 Z12 A90 F1000\nM30')
        self.page.locator('#simStage').select_option('sculpture')
        self.assertTrue(self.js('sg.length>0&&sg.every(g=>!g.h)'))
        self.page.locator('#simStage').select_option('pockets')
        self.assertTrue(self.js('sg.length>0&&sg.every(g=>g.h)'))
        self.page.locator('#simStage').select_option('all')
        self.assertTrue(self.js('sg.some(g=>g.h)&&sg.some(g=>!g.h)'))
        self.page.locator('#vm').select_option('2')
        self.assertIn('não é o resultado',self.page.locator('#viewStatus').text_content())
        self.assertTrue(self.js('FLD.every(r=>r===15)'))
        self.page.locator('#vm').select_option('1')
        self.assertIn('percursos',self.page.locator('#viewStatus').text_content())

    def test_pocket_floor_readout_uses_mach3_origin_without_moving_aspire(self):
        self.assertEqual(self.page.locator('#fz').input_value(),'9')
        self.page.locator('#Z0').select_option('1')
        self.assertEqual(self.page.locator('#fz').input_value(),'-6')
        self.assertIn('G1 Z-6',self.page.locator('#out').input_value())
        self.page.locator('#Z0').select_option('0')
        self.assertEqual(self.page.locator('#fz').input_value(),'9')
        self.assertIn('G1 Z9',self.page.locator('#out').input_value())

    def load_reference_stl(self):
        vertices=[(0,-8,-8),(0,8,-8),(0,8,8),(0,-8,8),(120,-8,-8),(120,8,-8),(120,8,8),(120,-8,8)]
        faces=[(0,1,2),(0,2,3),(4,6,5),(4,7,6),(0,4,5),(0,5,1),(3,2,6),(3,6,7),(0,3,7),(0,7,4),(1,5,6),(1,6,2)]
        text='solid target\n'+''.join('facet normal 0 0 0\nouter loop\n'+''.join('vertex %s %s %s\n'%vertices[i] for i in face)+'endloop\nendfacet\n' for face in faces)+'endsolid target'
        self.page.locator('#fst').set_input_files({'name':'target.stl','mimeType':'model/stl','buffer':text.encode()})
        self.page.wait_for_function('TRI!==null&&TGT!==null')

    def test_docks_pin_collapse_temporary_and_persistence(self):
        self.assertEqual(self.page.locator('main').get_attribute('data-left-pinned'),'true')
        self.page.screenshot(path='/tmp/makernauta-docks-pinned.png',full_page=True)
        initial=self.page.locator('#workspaceCenter').bounding_box()['width']
        self.page.locator('[data-panel-pin="left"]').click()
        self.page.wait_for_timeout(100)
        wider=self.page.locator('#workspaceCenter').bounding_box()['width']
        self.assertGreater(wider,initial+150)
        self.page.locator('[data-panel-pin="right"]').click()
        self.page.wait_for_timeout(100)
        self.assertGreater(self.page.locator('#workspaceCenter').bounding_box()['width'],wider+150)
        self.page.screenshot(path='/tmp/makernauta-docks-hidden.png',full_page=True)
        self.page.locator('[data-panel-tab="left"]').click()
        self.assertTrue(self.page.locator('#leftDock').is_visible())
        self.page.screenshot(path='/tmp/makernauta-dock-temporary.png')
        self.page.keyboard.press('Escape')
        self.assertFalse(self.page.locator('#leftDock').is_visible())
        self.page.locator('[data-panel-tab="right"]').click()
        self.page.locator('[data-panel-pin="right"]').click()
        self.assertEqual(self.page.locator('main').get_attribute('data-right-pinned'),'true')
        self.page.reload()
        self.page.wait_for_function('sg.length>0')
        self.assertEqual(self.page.locator('main').get_attribute('data-left-pinned'),'false')
        self.assertEqual(self.page.locator('main').get_attribute('data-right-pinned'),'true')
        self.page.locator('[data-panel-collapse="right"]').click()
        self.assertFalse(self.page.locator('#rightDock').is_visible())

    def test_accordions_preserve_values_and_are_independent_and_keyboard_accessible(self):
        self.page.locator('#T').fill('4')
        code=self.page.locator('#out').input_value()
        self.page.locator('#pocketSection > summary').focus()
        self.page.keyboard.press('Enter')
        self.assertFalse(self.page.locator('#pocketSection').evaluate('(e)=>e.open'))
        self.page.locator('#aspireSection > summary').click()
        self.assertFalse(self.page.locator('#aspireSection').evaluate('(e)=>e.open'))
        self.assertTrue(self.page.locator('#stlSection').evaluate('(e)=>e.open'))
        self.page.locator('#pocketSection > summary').click()
        self.assertEqual(self.page.locator('#T').input_value(),'4')
        self.assertEqual(self.page.locator('#out').input_value(),code)
        self.page.reload()
        self.assertFalse(self.page.locator('#aspireSection').evaluate('(e)=>e.open'))
        self.assertTrue(self.page.locator('#pocketSection').evaluate('(e)=>e.open'))

    def test_auxiliary_panels_and_resizing_preserve_simulation_and_camera(self):
        self.js("$('ql').value='0';draw();v3();tt=tot*.65;dr3();ya=.7;pa=.4;zm=1.3;window.savedField=FLD;window.savedValues=Array.from(FLD);window.savedTime=tt")
        for key in ['section','xy','tool','cut']:
            self.page.locator(f'[data-section="{key}"] > summary').click()
            self.assertLess(self.page.locator(f'[data-section="{key}"]').bounding_box()['height'],55)
        self.page.locator('[data-panel-pin="left"]').click()
        self.page.locator('[data-panel-pin="right"]').click()
        self.page.set_viewport_size({'width':1700,'height':1000})
        self.page.wait_for_timeout(150)
        self.assertTrue(self.js('FLD===savedField&&tt===savedTime&&savedValues.every((v,i)=>v===FLD[i])'))
        self.assertEqual(self.js('[ya,pa,zm]'),[.7,.4,1.3])
        self.page.screenshot(path='/tmp/makernauta-aux-collapsed.png',full_page=True)
        for key in ['section','xy','tool','cut']:
            self.page.locator(f'[data-section="{key}"] > summary').click()
        self.page.wait_for_timeout(100)
        self.assertTrue(self.js('FLD===savedField&&tt===savedTime'))
        self.assertTrue(self.js('LY.pw>0&&LY.ph>0'))

    def test_safety_modal_and_mobile_layout(self):
        self.page.locator('#safetyButton').click()
        self.assertTrue(self.page.locator('#safetyDialog').is_visible())
        self.assertIn('nunca foi testado numa CNC real',self.page.locator('#safetyDialog').text_content())
        self.page.keyboard.press('Escape')
        self.assertFalse(self.page.locator('#safetyDialog').is_visible())
        self.page.locator('#safetyButton').click()
        self.page.get_by_role('button',name='Fechar aviso',exact=True).click()
        self.page.set_viewport_size({'width':390,'height':844})
        self.page.wait_for_timeout(100)
        self.assertTrue(self.js('document.documentElement.scrollWidth<=innerWidth'))
        self.page.locator('[data-panel-pin="left"]').click()
        self.page.locator('[data-panel-tab="left"]').click()
        box=self.page.locator('#leftDock').bounding_box()
        self.assertGreaterEqual(box['x'],0)
        self.assertLessEqual(box['x']+box['width'],390)
        self.page.keyboard.press('Escape')
        self.page.screenshot(path='/tmp/makernauta-mobile-workspace.png',full_page=True)

    def test_stl_roughing_is_progressive_and_unwraps_without_fake_removal(self):
        self.js("$('ql').value='0';draw();v3();window.savedField=FLD")
        code=self.page.locator('#out').input_value()
        self.load_reference_stl()
        self.assertEqual(self.page.locator('#vm').input_value(),'4')
        self.assertEqual(self.page.locator('#out').input_value(),code)
        self.assertTrue(self.js('FLD===savedField&&FLD.every(r=>r===15)&&tt===0'))
        self.js('tt=tot*.55;dr3()')
        self.assertTrue(self.js('FLD.some(r=>r<15)&&tt>0'))
        self.page.locator('[data-section="simulation"]').screenshot(path='/tmp/makernauta-stl-roughing.png')
        self.js("window.beforeUnwrap=Array.from(FLD);window.beforeTime=tt;$('mo').value=0;$('mo').oninput()")
        self.assertTrue(self.js('VW.t===0&&tt===beforeTime&&beforeUnwrap.every((v,i)=>v===FLD[i])'))
        self.page.locator('[data-section="simulation"]').screenshot(path='/tmp/makernauta-stl-unwrapped.png')
        self.js("$('mo').value=100;$('mo').oninput();tt=tot;dr3()")
        self.page.locator('#rs3').click()
        self.assertTrue(self.js('tt===0&&FLD.every(r=>r===15)'))
        self.page.locator('#vm').select_option('2')
        self.page.locator('#pl3').click()
        self.assertEqual(self.page.locator('#vm').input_value(),'4')
        self.page.wait_for_timeout(150)
        self.assertGreater(self.js('tt'),0)
        self.page.locator('#pl3').click()
        self.assertFalse(self.js('pl'))
        self.js('ops.splice(0);lst();draw();v3();tt=tot;dr3()')
        self.assertTrue(self.js('FLD.every(r=>r===15)&&Object.keys(PK).length===0'))

    def test_stl_aspire_and_pocket_stages_and_per_operation_reference(self):
        self.load_reference_stl()
        self.page.locator('#ST').check()
        self.assertTrue(self.js('ops[0].stlDepth'))
        self.page.locator('#addC').click()
        self.assertFalse(self.page.locator('#ST').is_checked())
        self.page.locator('#list button').nth(0).click()
        self.assertTrue(self.page.locator('#ST').is_checked())
        self.page.locator('#ST').uncheck()
        self.page.locator('#sc').fill('(Z0 = centro)\nG21 G90 G17\nG0 X30 Y0 Z23 A0\nG1 Z11 F200\nG1 X60 A90 F1000\nG0 Z23\nM30')
        self.page.locator('#simStage').select_option('sculpture')
        self.js('tt=tot;dr3()')
        self.assertTrue(self.js('sg.every(g=>!g.h)&&FLD.some(r=>r<15)&&Object.keys(PK).length===0'))
        self.page.locator('#simStage').select_option('all')
        self.js('tt=tot;dr3()')
        self.assertTrue(self.js('sg.some(g=>g.h)&&sg.some(g=>!g.h)&&Object.keys(PK).length===2'))
        self.page.locator('[data-section="simulation"]').screenshot(path='/tmp/makernauta-stl-aspire-pockets.png')

    def test_machine_visuals_align_and_rotate_without_moving_tailstock(self):
        result=self.js('''() => {
          const a=machineVisualGeometry(P(),0,0),b=machineVisualGeometry(P(),-Math.PI/2,0),seam=mph(0,-Math.PI/2,P().D/2,1);
          return {jaws:a.jaws.length,left:a.faces.filter(f=>f.group==='chuck').every(f=>f.points.every(p=>p[0]<0)),right:a.faces.filter(f=>f.group==='tailstock').every(f=>f.points.every(p=>p[0]>P().L)),
            aligned:Math.hypot(b.jaws[0][1]-seam[1],b.jaws[0][2]-seam[2]),
            fixed:JSON.stringify(a.faces.filter(f=>f.group==='tailstock'))===JSON.stringify(b.faces.filter(f=>f.group==='tailstock'))};
        }''')
        self.assertEqual(result['jaws'],3)
        self.assertTrue(result['left'] and result['right'] and result['fixed'])
        self.assertLess(result['aligned'],1e-10)
        self.assertTrue(self.js('VW.machine!==null'))
        self.page.locator('[data-section="simulation"]').screenshot(path='/tmp/makernauta-machine-stock.png')
        self.js("$('mo').value=0;$('mo').oninput()")
        self.assertIsNone(self.js('VW.machine'))

    def test_stock_end_faces_are_solid_from_both_axis_directions(self):
        self.page.locator('#showMachine').uncheck()
        for angle in [-math.pi/2,math.pi/2]:
            color=self.page.evaluate('''angle=>{ya=angle;pa=0;zm=1;PX=0;PY=0;$('tp').checked=false;$('oc').checked=false;dr3();return Array.from(VW.g.getImageData(Math.round(VW.W/2),Math.round(VW.H/2),1,1).data)}''',angle)
            self.assertGreater(color[0],color[2]*1.3, f'End face should be amber, not background: {color}')
            self.assertEqual(color[3],255)
        self.page.locator('#c3').screenshot(path='/tmp/makernauta-solid-end.png')

    def test_vertical_resize_updates_canvas_and_preserves_state_and_nc(self):
        self.js("$('ql').value='0';draw();v3();tt=tot*.5;dr3();window.beforeResize={field:FLD,values:Array.from(FLD),time:tt,code:$('out').value,camera:[ya,pa,zm,PX,PY]}")
        handle=self.page.get_by_role('separator',name='Ajustar altura da simulação 3D')
        handle.scroll_into_view_if_needed()
        box=handle.bounding_box()
        self.page.mouse.move(box['x']+box['width']/2,box['y']+box['height']/2)
        self.page.mouse.down()
        self.page.mouse.move(box['x']+box['width']/2,box['y']+box['height']/2+180,steps=8)
        self.page.mouse.up()
        self.page.wait_for_timeout(100)
        self.assertGreater(self.page.locator('#simulationViewport').bounding_box()['height'],490)
        self.assertTrue(self.js('Math.abs(c3.height-c3.getBoundingClientRect().height*devicePixelRatio)<=1'))
        self.assertTrue(self.js("FLD===beforeResize.field&&beforeResize.values.every((v,i)=>v===FLD[i])&&tt===beforeResize.time&&$('out').value===beforeResize.code&&JSON.stringify([ya,pa,zm,PX,PY])===JSON.stringify(beforeResize.camera)"))
        self.page.locator('[data-panel-pin="left"]').click()
        self.page.locator('[data-panel-pin="right"]').click()
        handle.focus()
        self.page.keyboard.press('ArrowDown')
        self.page.wait_for_timeout(100)
        self.assertTrue(self.js("FLD===beforeResize.field&&tt===beforeResize.time&&$('out').value===beforeResize.code"))
        self.page.locator('[data-section="simulation"]').screenshot(path='/tmp/makernauta-machine-resized.png')
        height=handle.get_attribute('aria-valuenow')
        self.page.reload()
        self.page.wait_for_function('sg.length>0')
        self.assertEqual(self.page.get_by_role('separator').get_attribute('aria-valuenow'),height)

    def test_visual_fixture_toggle_preserves_removal_and_export_baselines(self):
        self.assertEqual(hashlib.sha256(self.page.locator('#out').input_value().encode()).hexdigest(),'3e5b3159db84a38fc62469a8437606a8f6f58dcb5d19877980a98f5672dfcb97')
        self.js("$('addR').click();$('T').value=4;$('T').oninput();$('addL').click();$('HT').value='1';$('HT').oninput();$('Z0').value='1';draw();v3()")
        self.assertEqual(hashlib.sha256(self.page.locator('#out').input_value().replace('Alojamento 3: linha','Alojamento 3: retangulo').encode()).hexdigest(),'bb2baf3f976a19cdd2c03d7170426b1d13abeebce14ecf9de57519078034175e')
        self.js("tt=tot;dr3();window.visualBefore={field:FLD,values:Array.from(FLD),code:$('out').value,path:JSON.stringify(sg)}")
        self.page.locator('#showMachine').uncheck()
        self.page.locator('#showMachine').check()
        self.assertTrue(self.js("FLD===visualBefore.field&&visualBefore.values.every((v,i)=>v===FLD[i])&&$('out').value===visualBefore.code&&JSON.stringify(sg)===visualBefore.path"))
        self.load_reference_stl()
        self.assertEqual(self.page.locator('#vm').input_value(),'4')
        self.assertTrue(self.js("FLD===visualBefore.field&&$('out').value===visualBefore.code"))
        self.page.locator('[data-section="simulation"]').screenshot(path='/tmp/makernauta-machine-stl.png')
        self.page.locator('#sc').fill('(Z0 = superficie do bruto)\nG21 G90 G17\nG0 X30 Z8 A0\nG1 Z-3 F200\nG1 X60 A90 F1000\nM30')
        self.page.locator('#simStage').select_option('sculpture')
        self.js('tt=tot*.8;dr3()')
        self.assertTrue(self.js('Math.abs(VW.machine.partAngle)>0&&Math.abs(VW.machine.machineAngle)<1e-10'))
        self.page.locator('[data-section="simulation"]').screenshot(path='/tmp/makernauta-machine-rotating.png')

    def test_height_control_mobile_hidpi_and_bounds(self):
        context=self.browser.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True)
        page=context.new_page()
        page.on('pageerror',lambda error:self.errors.append(str(error)))
        try:
            page.goto(self.url)
            page.wait_for_function('sg.length>0')
            handle=page.get_by_role('separator',name='Ajustar altura da simulação 3D')
            handle.scroll_into_view_if_needed()
            handle.focus()
            page.keyboard.press('End')
            page.wait_for_timeout(100)
            self.assertEqual(handle.get_attribute('aria-valuenow'),'1000')
            self.assertEqual(page.evaluate('c3.height'),2000)
            page.keyboard.press('Home')
            page.keyboard.press('ArrowUp')
            page.wait_for_timeout(100)
            self.assertEqual(handle.get_attribute('aria-valuenow'),'240')
            self.assertEqual(page.evaluate('c3.height'),480)
            self.assertTrue(page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
            page.locator('[data-section="simulation"]').screenshot(path='/tmp/makernauta-machine-mobile.png')
        finally:context.close()

    def test_visual_a_controls_never_change_program_or_material(self):
        self.js("tt=tot;dr3();window.beforeInspection={code:$('out').value,ops:JSON.stringify(ops),field:Array.from(FLD),time:tt,angle:VW.fo,tip:VW.machine.tailstockTip}")
        self.page.locator('#aRight').click()
        self.assertTrue(self.js("$('out').value===beforeInspection.code&&JSON.stringify(ops)===beforeInspection.ops&&tt===beforeInspection.time&&FLD.every((v,i)=>v===beforeInspection.field[i])"))
        self.assertAlmostEqual(self.js('VW.fo-beforeInspection.angle'),math.pi/12)
        self.assertEqual(self.js('VW.machine.tailstockTip'),self.js('beforeInspection.tip'))
        self.page.locator('#aLeft').click()
        self.assertEqual(self.js('inspectionA'),0)
        self.page.locator('#aRight').click()
        self.page.locator('#hm').click()
        self.assertEqual(self.js('inspectionA'),0)

    def test_section_titles_and_collapsed_panel_arrows(self):
        for title in self.page.locator('.dock summary').all_text_contents():
            self.assertRegex(title,r'^[^0-9]')
        for side in ['left','right']:
            self.page.locator(f'[data-panel-pin="{side}"]').click()
            tab=self.page.locator(f'[data-panel-tab="{side}"]')
            self.assertTrue(tab.is_visible())
            self.assertIn(tab.evaluate("el => getComputedStyle(el, '::before').content"),['"›"','"‹"'])
            tab.click()
            self.assertTrue(self.page.locator(f'[data-panel-pin="{side}"]').is_visible())
            self.page.keyboard.press('Escape')

    def test_spline_edit_drag_export_and_tools(self):
        self.page.locator('#addSpline').click()
        self.assertEqual(self.js('ops[sel].sp.length'),4)
        self.assertTrue(self.page.locator('#cm').is_disabled())
        self.page.locator('#splinePoints').fill('-10, 0\n-4, 6\n4, -6\n10, 0')
        self.page.wait_for_timeout(100)
        self.assertEqual(self.js('ops[sel].sp[1]'),[-4,6])
        self.assertIn('spline',self.page.locator('#out').input_value())
        self.assertTrue(self.js("sg.some(g=>g.h&&g.o===sel&&!g.r)"))
        # Generated cutting XY matches the sampled centerline after machine rounding.
        self.assertLess(self.js("Math.max(...splinePath(ops[sel]).map(p=>Math.min(...sg.filter(g=>g.h&&g.o===sel&&!g.r).map(g=>Math.hypot(g.q.x-ops[sel].x-p[0],g.q.y-p[1])))))"),.002)
        self.page.locator('#xy').scroll_into_view_if_needed()
        target=self.js("() => {const v=$('xy').splineProjection,p=ops[sel].sp[1],r=$('xy').getBoundingClientRect();return {x:r.left+v.cx+p[0]*v.sc,y:r.top+v.cy-p[1]*v.sc}}")
        self.page.mouse.move(target['x'],target['y']);self.page.mouse.down()
        self.page.mouse.move(target['x']+10,target['y']+8);self.page.mouse.up()
        self.assertNotEqual(self.js('ops[sel].sp[1]'),[-4,6])
        for tool in ['0','1']:
            self.js(f"ops[sel].toolType='{tool}';draw();v3();tt=tot;dr3()")
            self.assertTrue(self.js('FLD.every(Number.isFinite)&&FLD.some(v=>v<15)'))
        self.page.locator('#splinePoints').fill('0, 0')
        self.assertTrue(self.page.locator('#download').is_disabled())
        self.assertEqual(self.page.locator('#out').input_value(),'')
        self.page.locator('#d').fill('2')
        self.assertTrue(self.page.locator('#download').is_disabled())
        self.assertEqual(self.page.locator('#out').input_value(),'')
        self.page.locator('#splinePoints').fill('-10,0\n-5,4\n5,-4\n10,0')
        self.assertFalse(self.page.locator('#download').is_disabled())
        self.page.locator('[data-section="map"]').screenshot(path='/tmp/makernauta-spline.png')

    def test_spline_subdivision_bounds_and_degenerate_controls(self):
        error=self.js("""() => {let error=0;for(const sp of [[[-10,0],[-4,8],[4,-8],[10,0]],[[0,0],[20,0],[-20,0],[0,0]],[[0,0],[0,0],[0,0],[0,0]]]){const path=splinePath({sp});for(let n=0;n<=1000;n++){const t=n/1000,v=1-t,q=[0,1].map(k=>v*v*v*sp[0][k]+3*v*v*t*sp[1][k]+3*v*t*t*sp[2][k]+t*t*t*sp[3][k]);let best=Infinity;for(let i=1;i<path.length;i++){const a=path[i-1],b=path[i],dx=b[0]-a[0],dy=b[1]-a[1],l=dx*dx+dy*dy,u=l?Math.max(0,Math.min(1,((q[0]-a[0])*dx+(q[1]-a[1])*dy)/l)):0;best=Math.min(best,Math.hypot(q[0]-a[0]-u*dx,q[1]-a[1]-u*dy))}error=Math.max(error,best)}}return error}""")
        self.assertLessEqual(error,.03)

    def test_a30_crossing_cuts_final_mesh_single_surface_and_replay(self):
        result=self.js("""() => {
          $('D').value=30;$('L').value=120;$('ql').value='0';$('rf').value='0';$('oc').checked=false;$('tp').checked=false;$('showMachine').checked=false;
          ops.splice(0,ops.length,{t:'c',x:30,a:30,w:10,l:10,d:1},{t:'r',ln:true,cm:'on',x:70,a:30,w:3,l:20,rot:90,d:1.5},{t:'r',ln:true,cm:'on',x:60,a:30,w:3,l:20,rot:0,d:3});sel=0;draw();v3();tt=tot;dr3();
          const final=Array.from(FLD),floors=[30,70,60].map(x=>cutterRadiusAt(0,Math.PI/6,{x,y:0,z:x===30?14:x===70?13.5:12,a:30,zo:0,ad:1},{diameter:3,ball:false}));
          const g=m3.getContext('2d'),fill=g.fill,begin=g.beginPath,move=g.moveTo,line=g.lineTo,expected=(NXG-1)*NPG+2*NPG,edges=new Map();let count=0,points=[];
          g.beginPath=function(){points=[];return begin.apply(this,arguments)};g.moveTo=function(x,y){points.push([x,y]);return move.apply(this,arguments)};g.lineTo=function(x,y){points.push([x,y]);return line.apply(this,arguments)};
          g.fill=function(){if(count<expected){const vertices=points.map(p=>p.map(v=>v.toFixed(6)).join(','));for(let i=0;i<vertices.length;i++){const a=vertices[i],b=vertices[(i+1)%vertices.length];if(a!==b){const key=[a,b].sort().join('|');edges.set(key,(edges.get(key)||0)+1)}}}count++;return fill.apply(this,arguments)};dr3();g.fill=fill;g.beginPath=begin;g.moveTo=move;g.lineTo=line;
          const manifold=[...edges.values()].every(count=>count===2),stable=FLD.every((v,i)=>v===final[i]);tt=0;dr3();const reset=FLD.every(v=>v===15);tt=tot;dr3();const replay=FLD.every((v,i)=>v===final[i]);
          grid();for(let k=0;k<=20;k++){tt=tot*k/20;const p=curp();carveTo(p.ci,p.u)}const incremental=FLD.every((v,i)=>v===final[i]);dr3();
          return {count,expected,manifold,incremental,stable,reset,replay,floors,finite:FLD.every(v=>Number.isFinite(v)&&v>=0&&v<=15),min:Math.min(...FLD),code:$('out').value};
        }""")
        self.assertEqual(result['floors'],[14,13.5,12])
        self.assertTrue(result['finite'] and result['stable'] and result['reset'] and result['replay'] and result['incremental'])
        self.assertTrue(result['manifold'], 'Cada aresta da superfície fechada deve pertencer a duas faces')
        self.assertAlmostEqual(result['min'],12,places=4)
        # Cube fills three faces; no independent overlapping pocket grids remain.
        self.assertLessEqual(result['count']-result['expected'],3)
        self.assertIn('Alojamento 2: linha',result['code'])
        self.assertNotIn('retangulo',result['code'])
        self.page.locator('#c3').screenshot(path='/tmp/makernauta-a30-final.png')


    def test_a30_floors_on_all_three_operations_and_quality_levels(self):
        values=self.js("""() => {const results=[];$('D').value=30;$('L').value=120;$('rf').value='0';
          for(const quality of ['0','1','2'])for(const floor of [14,13.5,12]){
            $('ql').value=quality;ops.splice(0,ops.length,{t:'c',x:30,a:30,w:10,l:10,d:15-floor},{t:'r',ln:true,cm:'on',x:70,a:30,w:3,l:20,rot:90,d:15-floor},{t:'r',ln:true,cm:'on',x:60,a:30,w:3,l:20,rot:0,d:15-floor});draw();pg();grid();carveTo(sg.length-1,1);
            const j=Math.round(NPG/12),radii=[30,70,60].map(x=>FLD[Math.round(x/120*(NXG-1))*NPG+j]);results.push({floor,radii,finite:FLD.every(v=>Number.isFinite(v)&&v<=15&&v>=0)});
          }return results}""")
        for row in values:
            self.assertTrue(row['finite'])
            for radius in row['radii']:
                self.assertAlmostEqual(radius,row['floor'],delta=.001)

    def test_spline_mouse_click_creation_and_cancel_preserves_numeric_mode(self):
        self.page.locator('#addSpline').click()
        original=self.js('JSON.stringify(ops[sel].sp)')
        self.page.locator('#splineDraw').click()
        self.assertEqual(self.page.locator('#splineDraw').get_attribute('aria-pressed'),'true')
        self.assertTrue(self.page.locator('#xy').is_visible())
        canvas=self.page.locator('#xy')
        canvas.scroll_into_view_if_needed()
        bounds=canvas.bounding_box()
        for x,y in [(0.25,0.48),(0.40,0.20),(0.62,0.80),(0.76,0.5)]:
            self.page.mouse.click(bounds['x']+bounds['width']*x,bounds['y']+bounds['height']*y)
        self.assertEqual(self.page.locator('#splineDraw').get_attribute('aria-pressed'),'false')
        self.assertNotEqual(self.js('JSON.stringify(ops[sel].sp)'),original)
        self.assertIn('\n',self.page.locator('#splinePoints').input_value())
        self.assertFalse(self.page.locator('#download').is_disabled())
        edited=self.js('JSON.stringify(ops[sel].sp)')
        self.page.locator('#splineDraw').click()
        self.page.mouse.click(bounds['x']+bounds['width']*.36,bounds['y']+bounds['height']*.40)
        self.assertEqual(self.js('JSON.stringify(ops[sel].sp)'),edited)
        self.page.keyboard.press('Escape')
        self.assertEqual(self.js('JSON.stringify(ops[sel].sp)'),edited)
        self.assertEqual(self.page.locator('#splineDraw').get_attribute('aria-pressed'),'false')
        self.page.locator('#splinePoints').fill('-10,0\n-5,4\n5,-4\n10,0')
        self.assertEqual(self.js('ops[sel].sp[1]'),[-5,4])

    def test_cylinder_cut_angle_matches_tool_and_contour_in_rolled_view(self):
        result=self.js("""() => {
          const tool={diameter:3,ball:false},q={x:35,y:0,z:12,a:30,zo:0,ad:1};
          const front=cutterRadiusAt(0,Math.PI/6,q,tool);
          const opposite=cutterRadiusAt(0,-Math.PI/6,q,tool);
          const projected=mpt(q,1,0),radius=Math.atan2(projected[1],projected[2]);
          $('D').value=30;$('L').value=120;$('ql').value='2';
          ops.splice(0,ops.length,{t:'r',ln:true,cm:'on',x:60,a:30,w:3,l:20,d:3});
          sel=0;draw();pg();grid();carveTo(sg.length-1,1);
          const x=Math.round(60/120*(NXG-1)),j=Math.round(NPG/12),jWrong=Math.round(NPG*11/12);
          return {front,opposite,radius,cut:FLD[x*NPG+j],wrong:FLD[x*NPG+jWrong],code:$('out').value};
        }""")
        self.assertAlmostEqual(result['front'],12,places=4)
        self.assertTrue(not math.isfinite(result['opposite']) or result['opposite']>12.5)
        self.assertAlmostEqual(result['radius'],math.pi/6,places=4)
        self.assertLess(result['cut'],13)
        self.assertGreater(result['wrong'],result['cut']+.5)
        self.assertIn('G0 A30',result['code'])

    def test_invalid_step_cannot_hang_generation(self):
        self.page.locator('#SD').fill('0')
        self.assertEqual(self.page.locator('#out').input_value(),'')
        self.assertIn('maiores que zero', self.page.locator('#err').text_content())


if __name__ == '__main__':
    unittest.main()
