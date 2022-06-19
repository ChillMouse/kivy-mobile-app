#!/usr/bin/kivy
from App.Controller.app import *

if __name__ in ('__main__', '__android__'):
    app_etalina = EtalinaApp()
    app_etalina.run()