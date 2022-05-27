PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE col
(
    id     integer primary key,
    crt    integer not null,
    mod    integer not null,
    scm    integer not null,
    ver    integer not null,
    dty    integer not null,
    usn    integer not null,
    ls     integer not null,
    conf   text    not null,
    models text    not null,
    decks  text    not null,
    dconf  text    not null,
    tags   text    not null
);
INSERT INTO col VALUES(1,1442476800,1653683608168,1653683608163,11,0,0,0,'{"schedVer":1,"sortBackwards":false,"nextPos":1,"newSpread":0,"addToCur":true,"estTimes":true,"collapseTime":1200,"sortType":"noteFld","timeLim":0,"dueCounts":true,"curDeck":1,"dayLearnFirst":false,"curModel":1376926904739,"activeDecks":[1]}','{"1376926904739":{"id":1376926904739,"name":"Basic-669e0","type":0,"mod":1653683567,"usn":-1,"sortf":0,"did":1653683537446,"tmpls":[{"name":"Card 1","ord":0,"qfmt":"{{Front}}","afmt":"{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}","bqfmt":"","bafmt":"","did":null,"bfont":"","bsize":0}],"flds":[{"name":"Front","ord":0,"sticky":false,"rtl":false,"font":"Arial","size":20,"media":[],"description":""},{"name":"Back","ord":1,"sticky":false,"rtl":false,"font":"Arial","size":20,"media":[],"description":""}],"css":".card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n","latexPre":"\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage[utf8]{inputenc}\n\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n","latexPost":"\\end{document}","latexsvg":false,"req":[[0,"any",[0]]],"tags":["created-with-braindb"],"vers":[]},"1653683608163":{"id":1653683608163,"name":"Basic","type":0,"mod":0,"usn":0,"sortf":0,"did":1,"tmpls":[{"name":"Card 1","ord":0,"qfmt":"{{Front}}","afmt":"{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}","bqfmt":"","bafmt":"","did":null,"bfont":"","bsize":0}],"flds":[{"name":"Front","ord":0,"sticky":false,"rtl":false,"font":"Arial","size":20},{"name":"Back","ord":1,"sticky":false,"rtl":false,"font":"Arial","size":20}],"css":".card {\n  font-family: arial;\n  font-size: 20px;\n  text-align: center;\n  color: black;\n  background-color: white;\n}\n","latexPre":"\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage[utf8]{inputenc}\n\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n","latexPost":"\\end{document}","latexsvg":false,"req":[[0,"any",[0]]]}}','{"1653683537446":{"id":1653683537446,"mod":1653683537,"name":"BrainDB Deck","usn":-1,"lrnToday":[0,0],"revToday":[0,0],"newToday":[0,0],"timeToday":[0,0],"collapsed":false,"browserCollapsed":false,"desc":"","dyn":0,"conf":1,"extendNew":0,"extendRev":0},"1":{"id":1,"mod":0,"name":"Default","usn":0,"lrnToday":[0,0],"revToday":[0,0],"newToday":[0,0],"timeToday":[0,0],"collapsed":false,"browserCollapsed":false,"desc":"","dyn":0,"conf":1,"extendNew":0,"extendRev":0}}','{"1":{"id":1,"mod":0,"name":"Default","usn":0,"maxTaken":60,"autoplay":true,"timer":0,"replayq":true,"new":{"bury":false,"delays":[1.0,10.0],"initialFactor":2500,"ints":[1,4,0],"order":1,"perDay":20},"rev":{"bury":false,"ease4":1.3,"ivlFct":1.0,"maxIvl":36500,"perDay":200,"hardFactor":1.2},"lapse":{"delays":[10.0],"leechAction":1,"leechFails":8,"minInt":1,"mult":0.0},"dyn":false}}','{}');
CREATE TABLE notes
(
    id    integer primary key,
    guid  text    not null,
    mid   integer not null,
    mod   integer not null,
    usn   integer not null,
    tags  text    not null,
    flds  text    not null,
    sfld  integer not null,
    csum  integer not null,
    flags integer not null,
    data  text    not null
);
INSERT INTO notes VALUES(1653683561708,'eB[BHB5POk',1376926904739,1653683561,-1,' created-with-braindb ','(Front)(Back)','(Front)',4251924563,0,'');
INSERT INTO notes VALUES(1653683567089,'i/!cN}k~:}',1376926904739,1653683567,-1,' created-with-braindb ','(Front 2)(Back 2)','(Front 2)',945259959,0,'');
CREATE TABLE cards
(
    id     integer primary key,
    nid    integer not null,
    did    integer not null,
    ord    integer not null,
    mod    integer not null,
    usn    integer not null,
    type   integer not null,
    queue  integer not null,
    due    integer not null,
    ivl    integer not null,
    factor integer not null,
    reps   integer not null,
    lapses integer not null,
    left   integer not null,
    odue   integer not null,
    odid   integer not null,
    flags  integer not null,
    data   text    not null
);
INSERT INTO cards VALUES(1653683561709,1653683561708,1653683537446,0,1653683561,-1,0,0,29355,0,0,0,0,0,0,0,0,'');
INSERT INTO cards VALUES(1653683567090,1653683567089,1653683537446,0,1653683567,-1,0,0,29356,0,0,0,0,0,0,0,0,'');
CREATE TABLE revlog
(
    id      integer primary key,
    cid     integer not null,
    usn     integer not null,
    ease    integer not null,
    ivl     integer not null,
    lastIvl integer not null,
    factor  integer not null,
    time    integer not null,
    type    integer not null
);
CREATE TABLE graves
(
    usn  integer not null,
    oid  integer not null,
    type integer not null
);
ANALYZE sqlite_schema;
INSERT INTO sqlite_stat1 VALUES('col',NULL,'1');
ANALYZE sqlite_schema;
CREATE INDEX ix_notes_usn on notes (usn);
CREATE INDEX ix_cards_usn on cards (usn);
CREATE INDEX ix_revlog_usn on revlog (usn);
CREATE INDEX ix_cards_nid on cards (nid);
CREATE INDEX ix_cards_sched on cards (did, queue, due);
CREATE INDEX ix_revlog_cid on revlog (cid);
CREATE INDEX ix_notes_csum on notes (csum);
COMMIT;