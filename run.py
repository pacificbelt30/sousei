# -*- coding: utf-8 -*-
import sys
import app
if __name__=='__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == '-mb':
        app.makedb()
    else: app.run()

