# -*- coding: utf-8 -*-
import sys
import app
if __name__=='__main__':
    testflag = 'True' # テストデータを入れるフラグ
    if len(sys.argv) >= 2 and sys.argv[1] == '-mb':
        app.makedb(testflag)
    else: app.run()

