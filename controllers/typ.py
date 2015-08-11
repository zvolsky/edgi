# -*- coding: utf-8 -*-

from mzwwp import easy_search

def edit():
    '''grid prvků daného typu'''
    def before_grid_edit(typ_id, typ):
        def set_editable(condition, fld):
            if condition:
                fld.readable = fld.writable = True

        # filtrovaný validátor - výrobci jen pro zvolený typ prvku
        db.cis_prvek.vyrobce_id.requires = IS_IN_DB(db(db.vyrobce.cis_typ_prvku_id==typ_id), 'vyrobce.id', '%(vyrobce)s')
        # změnit údaje na editovatelné podle nastavení pro zvolený typ
        set_editable(typ.zadat_prorez, db.cis_prvek.prorez)
        set_editable(typ.zadat_delku, db.cis_prvek.delka)
        set_editable(typ.zadat_sirku, db.cis_prvek.sirka)

    return _grid(J("sortiment"), db.cis_prvek, before_grid=before_grid_edit)

def made():
    '''grid výrobců daného typu prvků'''
    return _grid(J("výrobci"), db.vyrobce)

def _grid(titulek, tbl, before_grid=None):
    typ_id, typ = _validate_typ()
    tbl.id.readable = False                 # skrýt id
    tbl.cis_typ_prvku_id.default = typ_id   # vložený záznam nechť má cis_typ_prvku podle aktuální filtrace pomocí URL args
    if before_grid:
        before_grid(typ_id, typ)
    grid = SQLFORM.grid(tbl.cis_typ_prvku_id==typ_id,
                        args=request.args[:1],
                        deletable=False,
                        showbuttontext=False)
    easy_search(grid)
    return dict(titulek="%s - %s" % ((typ.mnozne or typ.typ).capitalize(), titulek), grid=grid)

def _validate_typ():
    try:
        typ_id = int(request.args(0))
        typ = db.cis_typ_prvku[typ_id]
        if typ is not None:
            return typ_id, typ
    except:
        pass
    raise HTTP(404)
