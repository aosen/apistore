# -*- coding: utf-8 -*-
import traceback

def checkHave(func):
    def wrapper(*args, **kwargs):
        sql, db, argument= func(*args, **kwargs)
        try:
            result = db.get(sql, argument)
        except Exception as e:
            return None
        else:
            return result
    return wrapper

def cache_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print ("[****************************************************]")
            err = "{0}\n{1}".format(str(e), traceback.format_exc())
            print e
            print(err)
            #print args[1]
            print ("[****************************************************]")
        return err
    return wrapper
