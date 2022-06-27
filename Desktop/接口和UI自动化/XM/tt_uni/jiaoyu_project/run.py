import unittest
from unittestreport import TestRunner
from BeautifulReport import BeautifulReport
from common.handle_path import case_dir, reports_dir

# suite = unittest.defaultTestLoader.discover(case_dir)
#
# runner = TestRunner(suite,
#                     filename="zoume6.06.html",
#                     report_dir=reports_dir
#                     )

#另外一种生成报告的方式：
suite = unittest.defaultTestLoader.discover(case_dir)
runner = BeautifulReport(suites=suite)
runner.report('智慧教育自动化用例', filename='jiaoyue6.21.html',
             report_dir=reports_dir)




