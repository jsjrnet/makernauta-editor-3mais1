"""Browser and geometry regressions for the self-contained original editor.
Run: python3 -m unittest discover -s tests -v
Requires Playwright and Chromium (CHROMIUM_PATH optionally selects a system build).
These checks validate software behavior, never physical machining safety.
"""
import functools
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
        self.assertEqual(self.page.locator('canvas').count(), 4)
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
          $('TS').value=6;$('TY').value='1';$('T').value=2;$('HT').value='0';
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
        self.assertTrue(self.js("() => {$('TY').value='0';$('HT').value='1';return !toolFor({h:0}).ball&&toolFor({h:1}).ball}"))

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
        self.js("$('HT').value='1';draw();v3();tt=tot;dr3()")
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

    def test_aspire_xza_import_phase_tools_and_combined_mach3(self):
        code = '(Aspire XZA)\nG21 G90 G17\nG0 X10 Y0 Z23 A0\nS18000 M3\nG1 X20 Z12 A90 F1000\ng1 x30 z11 a180\nN100 M30\n'
        self.page.locator('#fsc').set_input_files({'name':'aspire.nc','mimeType':'text/plain','buffer':code.encode()})
        self.page.wait_for_function("$('si').textContent.startsWith('Lido:')")
        self.page.wait_for_timeout(250)
        output = self.page.locator('#out').input_value()
        self.assertIn('FIM DA ESCULTURA', output)
        self.assertIn('M0 (Troque a fresa e confirme)', output)
        self.assertEqual(output.count('M30'), 1)
        self.assertTrue(self.js('sg.some(s=>!s.h&&s.q.a===180)&&sg.some(s=>s.h)'))
        self.assertTrue(self.js('sg.some(s=>!s.h&&!toolFor(s).ball===false)'))
        self.page.locator('#OM').select_option('0')
        self.page.wait_for_timeout(250)
        self.assertNotIn('FIM DA ESCULTURA', self.page.locator('#out').input_value())
        self.assertTrue(self.js('sg.every(s=>s.h)'))

    def test_ascii_and_binary_stl_import_rotation_and_surface_floor(self):
        vertices=[(0,-5,-5),(0,5,-5),(0,5,5),(0,-5,5),(40,-5,-5),(40,5,-5),(40,5,5),(40,-5,5)]
        faces=[(0,1,2),(0,2,3),(4,6,5),(4,7,6),(0,4,5),(0,5,1),(3,2,6),(3,6,7),(0,3,7),(0,7,4),(1,5,6),(1,6,2)]
        ascii_stl='solid target\n'+''.join('facet normal 0 0 0\nouter loop\n'+''.join('vertex %s %s %s\n'%vertices[i] for i in face)+'endloop\nendfacet\n' for face in faces)+'endsolid target'
        binary=bytearray(80)+struct.pack('<I',len(faces))
        for face in faces:
            binary+=struct.pack('<12fH',0,0,0,*(v for i in face for v in vertices[i]),0)
        for name,data in [('ascii.stl',ascii_stl.encode()),('binary.stl',bytes(binary))]:
            self.page.locator('#fst').set_input_files({'name':name,'mimeType':'model/stl','buffer':data})
            self.page.wait_for_function("$('sti').textContent.startsWith('STL lido:')")
            self.assertEqual(self.js('TRI.length/9'),12)
            self.assertEqual(self.js('TLEN'),40)
            self.assertGreater(self.js('Math.max(...TGT)'),5)
        self.page.locator('#fit').click()
        self.assertEqual(self.page.locator('#L').input_value(),'40')
        self.page.locator('#SR').fill('90')
        self.page.locator('#SR').dispatch_event('change')
        self.page.locator('#SX').check()
        self.page.wait_for_timeout(100)
        self.assertIn('/90/true', self.js('GK'))

    def test_invalid_step_cannot_hang_generation(self):
        self.page.locator('#SD').fill('0')
        self.assertEqual(self.page.locator('#out').input_value(),'')
        self.assertIn('maiores que zero', self.page.locator('#err').text_content())


if __name__ == '__main__':
    unittest.main()
