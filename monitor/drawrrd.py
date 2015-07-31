#!/usr/bin/env python
#coding=utf-8
import rrdtool

def dItem01(data):
	pngname = str(data['pname'])
	start = data['stime']
	graphname = str(data['gname'] + " (" + data['graphid'] + ") " + data['host'] + "(" + data['flag'] + ")")
	DEF = str(r"DEF:a="+data['rrdpath']+r':'+data['pitem'][0][0]+r":AVERAGE")
	if data['cols'] or data['itypes']:
		if not data['cols']:
			dtype = str(data['itypes'][0][0]+r":a#EAAF00FF:"+data['pitem'][0][1])
		elif not data['itypes']:
			dtype = str(r"AREA:a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
		else:
			dtype = str(data['itypes'][0][0]+r":a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
	else:
		dtype = str(r"AREA:a#EAAF00FF:"+data['pitem'][0][1])
	unit = str(data['pitem'][0][2])
	if not unit:
		unit = ' '
	max = 'GPRINT:a:MAX:Max\:%.2lf %s'
	min = 'GPRINT:a:MIN:Min\:%.2lf %s'
	avg = 'GPRINT:a:AVERAGE:Avg\:%.2lf %s'
	now = 'GPRINT:a:LAST:Now\:%.2lf %s'
	if data['flag'] == 'Daily':
		rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start, '-x', 'MINUTE:30:HOUR:2:HOUR:2:0:%H:%M',
					'-t', graphname, '-v', unit, DEF, 'COMMENT: \\n', dtype, now, avg, min, max, 'COMMENT: \\n')
	elif data['flag'] == 'Weekly':
		rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start, '-x', 'HOUR:4:HOUR:12:DAY:1:0:%d',
					'-t', graphname, '-v', unit, DEF, 'COMMENT: \\n', dtype, now, avg, min, max, 'COMMENT: \\n')
	else:
		rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start,
					'-t', graphname, '-v', unit, DEF, 'COMMENT: \\n', dtype, now, avg, min, max, 'COMMENT: \\n')
		
###################################################################################################################
def dItem02(data):
	pngname = str(data['pname'])
	start = data['stime']
	graphname = str(data['gname'] + " (" + data['graphid'] + ") " + data['host'] + "(" + data['flag'] + ")")
	DEFa = str(r"DEF:a="+data['rrdpath']+r':'+data['pitem'][0][0]+r":AVERAGE")
	DEFb = str(r"DEF:b="+data['rrdpath']+r':'+data['pitem'][1][0]+r":AVERAGE")
	unit = str(data['pitem'][0][2])
	if not unit:
		unit = ' '
	if data['cols'] or data['itypes']:
		if not data['cols']:
			dtypea = str(data['itypes'][0][0]+r":a#00CF00FF:"+data['pitem'][0][1])
			dtypeb = str(data['itypes'][0][1]+r":b#002A97FF:"+data['pitem'][1][1])
		elif not data['itypes']:
			dtypea = str(r"AREA:a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
			dtypeb = str(r"LINE1:b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
		else:
			dtypea = str(data['itypes'][0][0]+r":a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
			dtypeb = str(data['itypes'][0][1]+r":b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
	else:
	#增加的代码主要是为硬盘使用情况做stack，而且由于swap与disk的use与free的item顺序不同还得判断颜色
		if 'Disk space' in data['gname'] or 'Swap' in data['gname']:
			if 'Disk space' in data['gname']:
				dtypea = str(r"AREA:a#862F2FFF:"+data['pitem'][0][1]+r":STACK")
				dtypeb = str(r"AREA:b#74C366FF:"+data['pitem'][1][1]+r":STACK")
			else:
				dtypea = str(r"AREA:a#74C366FF:"+data['pitem'][0][1]+r":STACK")
				dtypeb = str(r"AREA:b#862F2FFF:"+data['pitem'][1][1]+r":STACK")
		else:
			dtypea = str(r"AREA:a#00CF00FF:"+data['pitem'][0][1])
			dtypeb = str(r"LINE1:b#002A97FF:"+data['pitem'][1][1])
	maxa = 'GPRINT:a:MAX:Max\:%.2lf %s'
	mina = 'GPRINT:a:MIN:Min\:%.2lf %s'
	avga = 'GPRINT:a:AVERAGE:Avg\:%.2lf %s'
	nowa = 'GPRINT:a:LAST:Now\:%.2lf %s'
	maxb = 'GPRINT:b:MAX:Max\:%.2lf %s'
	minb = 'GPRINT:b:MIN:Min\:%.2lf %s'
	avgb = 'GPRINT:b:AVERAGE:Avg\:%.2lf %s'
	nowb = 'GPRINT:b:LAST:Now\:%.2lf %s'
	if 'Swap' in data['gname']:
		if data['flag'] == 'Daily':
			rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start, '-x', 'MINUTE:30:HOUR:2:HOUR:2:0:%H:%M',
						'-t', graphname, '-v', unit, DEFa, DEFb, 'COMMENT: \\n', dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', 
						dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n')
		elif data['flag'] == 'Weekly':
			rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start, '-x', 'HOUR:4:HOUR:12:DAY:1:0:%d',
						'-t', graphname, '-v', unit, DEFa, DEFb, 'COMMENT: \\n', dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', 
						dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n')
		else:
			rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start,
						'-t', graphname, '-v', unit, DEFa, DEFb, 'COMMENT: \\n', dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', 
						dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n')
	else:
		if data['flag'] == 'Daily':
			rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start, '-x', 'MINUTE:30:HOUR:2:HOUR:2:0:%H:%M',
						'-t', graphname, '-v', unit, DEFa, DEFb, 'COMMENT: \\n', dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n', 
						dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n')
		elif data['flag'] == 'Weekly':
			rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start, '-x', 'HOUR:4:HOUR:12:DAY:1:0:%d',
						'-t', graphname, '-v', unit, DEFa, DEFb, 'COMMENT: \\n', dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n', 
						dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n')
		else:
			rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start,
						'-t', graphname, '-v', unit, DEFa, DEFb, 'COMMENT: \\n', dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n', 
						dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n')
#################################################################################################################
def dItem03(data):
	pngname = str(data['pname'])
	start = data['stime']
	graphname = str(data['gname'] + " (" + data['graphid'] + ") " + data['host'] + "(" + data['flag'] + ")")
	DEFa = str(r"DEF:a="+data['rrdpath']+r':'+data['pitem'][0][0]+r":AVERAGE")
	DEFb = str(r"DEF:b="+data['rrdpath']+r':'+data['pitem'][1][0]+r":AVERAGE")
	DEFc = str(r"DEF:c="+data['rrdpath']+r':'+data['pitem'][2][0]+r":AVERAGE")
	unit = str(data['pitem'][0][2])
	if not unit:
		unit = ' '
	if data['cols'] or data['itypes']:
		if not data['cols']:
			dtypea = str(data['itypes'][0][0]+r":a#008A6DFF:"+data['pitem'][0][1])
			dtypeb = str(data['itypes'][0][1]+r":b#0000FFFF:"+data['pitem'][1][1])
			dtypec = str(data['itypes'][0][2]+r":c#6EA100FF:"+data['pitem'][2][1])
		elif not data['itypes']:
			dtypea = str(r"LINE1:a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
			dtypeb = str(r"LINE1:b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
			dtypec = str(r"LINE1:c"+data['cols'][0][2]+r":"+data['pitem'][2][1])
		else:
			dtypea = str(data['itypes'][0][0]+r":a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
			dtypeb = str(data['itypes'][0][1]+r":b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
			dtypec = str(data['itypes'][0][2]+r":c"+data['cols'][0][2]+r":"+data['pitem'][2][1])
	else:
		dtypea = str(r"LINE1:a#008A6DFF:"+data['pitem'][0][1])
		dtypeb = str(r"LINE1:b#0000FFFF:"+data['pitem'][1][1])
		dtypec = str(r"LINE1:c#6EA100FF:"+data['pitem'][2][1])
	maxa = 'GPRINT:a:MAX:Max\:%.2lf %s'
	mina = 'GPRINT:a:MIN:Min\:%.2lf %s'
	avga = 'GPRINT:a:AVERAGE:Avg\:%.2lf %s'
	nowa = 'GPRINT:a:LAST:Now\:%.2lf %s'
	maxb = 'GPRINT:b:MAX:Max\:%.2lf %s'
	minb = 'GPRINT:b:MIN:Min\:%.2lf %s'
	avgb = 'GPRINT:b:AVERAGE:Avg\:%.2lf %s'
	nowb = 'GPRINT:b:LAST:Now\:%.2lf %s'
	maxc = 'GPRINT:c:MAX:Max\:%.2lf %s'
	minc = 'GPRINT:c:MIN:Min\:%.2lf %s'
	avgc = 'GPRINT:c:AVERAGE:Avg\:%.2lf %s'
	nowc = 'GPRINT:c:LAST:Now\:%.2lf %s'
	if data['flag'] == 'Daily':
		rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start, '-x', 'MINUTE:30:HOUR:2:HOUR:2:0:%H:%M',
					'-t', graphname, '-v', unit, DEFa, DEFb, DEFc, 'COMMENT: \\n', dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n', 
					dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n')
	elif data['flag'] == 'Weekly':
		rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start, '-x', 'HOUR:4:HOUR:12:DAY:1:0:%d',
					'-t', graphname, '-v', unit, DEFa, DEFb, DEFc, 'COMMENT: \\n', dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n', 
					dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n')
	else:
		rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start,
					'-t', graphname, '-v', unit, DEFa, DEFb, DEFc, 'COMMENT: \\n', dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n', 
					dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n')
###############################################################################################################
def dItem04(data):
	pngname = str(data['pname'])
	start = data['stime']
	graphname = str(data['gname'] + " (" + data['graphid'] + ") " + data['host'] + "(" + data['flag'] + ")")
	DEFa = str(r"DEF:a="+data['rrdpath']+r':'+data['pitem'][0][0]+r":AVERAGE")
	DEFb = str(r"DEF:b="+data['rrdpath']+r':'+data['pitem'][1][0]+r":AVERAGE")
	DEFc = str(r"DEF:c="+data['rrdpath']+r':'+data['pitem'][2][0]+r":AVERAGE")
	DEFd = str(r"DEF:d="+data['rrdpath']+r':'+data['pitem'][3][0]+r":AVERAGE")
	unit = str(data['pitem'][0][2])
	if not unit:
		unit = ' '
	if data['cols'] or data['itypes']:
		if not data['cols']:
			dtypea = str(data['itypes'][0][0]+r":a#005D57FF:"+data['pitem'][0][1])
			dtypeb = str(data['itypes'][0][1]+r":b#4444FFFF:"+data['pitem'][1][1])
			dtypec = str(data['itypes'][0][2]+r":c#F24AC8FF:"+data['pitem'][2][1])
			dtyped = str(data['itypes'][0][3]+r":d#00CF00FF:"+data['pitem'][3][1])
		elif not data['itypes']:
			dtypea = str(r"LINE1:a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
			dtypeb = str(r"LINE1:b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
			dtypec = str(r"LINE1:c"+data['cols'][0][2]+r":"+data['pitem'][2][1])
			dtyped = str(r"LINE1:d"+data['cols'][0][3]+r":"+data['pitem'][3][1])
		else:
			dtypea = str(data['itypes'][0][0]+r":a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
			dtypeb = str(data['itypes'][0][1]+r":b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
			dtypec = str(data['itypes'][0][2]+r":c"+data['cols'][0][2]+r":"+data['pitem'][2][1])
			dtyped = str(data['itypes'][0][3]+r":d"+data['cols'][0][3]+r":"+data['pitem'][3][1])
	else:
		dtypea = str(r"LINE1:a#005D57FF:"+data['pitem'][0][1])
		dtypeb = str(r"LINE1:b#4444FFFF:"+data['pitem'][1][1])
		dtypec = str(r"LINE1:c#F24AC8FF:"+data['pitem'][2][1])
		dtyped = str(r"LINE1:d#00CF00FF:"+data['pitem'][3][1])
	maxa = 'GPRINT:a:MAX:Max\:%.2lf %s'
	mina = 'GPRINT:a:MIN:Min\:%.2lf %s'
	avga = 'GPRINT:a:AVERAGE:Avg\:%.2lf %s'
	nowa = 'GPRINT:a:LAST:Now\:%.2lf %s'
	maxb = 'GPRINT:b:MAX:Max\:%.2lf %s'
	minb = 'GPRINT:b:MIN:Min\:%.2lf %s'
	avgb = 'GPRINT:b:AVERAGE:Avg\:%.2lf %s'
	nowb = 'GPRINT:b:LAST:Now\:%.2lf %s'
	maxc = 'GPRINT:c:MAX:Max\:%.2lf %s'
	minc = 'GPRINT:c:MIN:Min\:%.2lf %s'
	avgc = 'GPRINT:c:AVERAGE:Avg\:%.2lf %s'
	nowc = 'GPRINT:c:LAST:Now\:%.2lf %s'
	maxd = 'GPRINT:d:MAX:Max\:%.2lf %s'
	mind = 'GPRINT:d:MIN:Min\:%.2lf %s'
	avgd = 'GPRINT:d:AVERAGE:Avg\:%.2lf %s'
	nowd = 'GPRINT:d:LAST:Now\:%.2lf %s'
	if data['flag'] == 'Daily':
		rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start, '-x', 'MINUTE:30:HOUR:2:HOUR:2:0:%H:%M',
					'-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, 'COMMENT: \\n', dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n', 
					dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
					dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n')
	elif data['flag'] == 'Weekly':
		rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start, '-x', 'HOUR:4:HOUR:12:DAY:1:0:%d',
					'-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, 'COMMENT: \\n', dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n', 
					dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
					dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n')
	else:
		rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start,
					'-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, 'COMMENT: \\n', dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n', 
					dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
					dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n')
############################################################################################3
def dItem05(data):
	pngname = str(data['pname'])
	start = data['stime']
	graphname = str(data['gname'] + " (" + data['graphid'] + ") " + data['host'] + "(" + data['flag'] + ")")
	DEFa = str(r"DEF:a="+data['rrdpath']+r':'+data['pitem'][0][0]+r":AVERAGE")
	DEFb = str(r"DEF:b="+data['rrdpath']+r':'+data['pitem'][1][0]+r":AVERAGE")
	DEFc = str(r"DEF:c="+data['rrdpath']+r':'+data['pitem'][2][0]+r":AVERAGE")
	DEFd = str(r"DEF:d="+data['rrdpath']+r':'+data['pitem'][3][0]+r":AVERAGE")
	DEFe = str(r"DEF:e="+data['rrdpath']+r':'+data['pitem'][4][0]+r":AVERAGE")
	if data['gname'] == 'Memory':
		cdefa = r"CDEF:cdefa=a,b,c,+,-"
	unit = str(data['pitem'][0][2])
	if not unit:
		unit = ' '
	if data['cols'] or data['itypes']:
		if not data['cols']:
			dtypea = str(data['itypes'][0][0]+r":a#862F2FFF:"+data['pitem'][0][1])
			dtypeb = str(data['itypes'][0][1]+r":b#EA8F00FF:"+data['pitem'][1][1])
			dtypec = str(data['itypes'][0][2]+r":c#FFC73BFF:"+data['pitem'][2][1])
			dtyped = str(data['itypes'][0][3]+r":d#74C366FF:"+data['pitem'][3][1])
			dtypee = str(data['itypes'][0][4]+r":e#FFC3C0FF:"+data['pitem'][4][1])
		elif not data['itypes']:
			dtypea = str(r"LINE1:a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
			dtypeb = str(r"LINE1:b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
			dtypec = str(r"LINE1:c"+data['cols'][0][2]+r":"+data['pitem'][2][1])
			dtyped = str(r"LINE1:d"+data['cols'][0][3]+r":"+data['pitem'][3][1])
			dtypee = str(r"LINE1:e"+data['cols'][0][4]+r":"+data['pitem'][4][1])
		else:
			dtypea = str(data['itypes'][0][0]+r":a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
			dtypeb = str(data['itypes'][0][1]+r":b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
			dtypec = str(data['itypes'][0][2]+r":c"+data['cols'][0][2]+r":"+data['pitem'][2][1])
			dtyped = str(data['itypes'][0][3]+r":d"+data['cols'][0][3]+r":"+data['pitem'][3][1])
			dtypee = str(data['itypes'][0][4]+r":e"+data['cols'][0][4]+r":"+data['pitem'][4][1])
	else:
		if data['gname'] == 'Memory':
			dtypea = str(r"AREA:cdefa#862F2FFF:"+data['pitem'][0][1]+r":STACK")
			dtypeb = str(r"AREA:b#EA8F00FF:"+data['pitem'][1][1]+r":STACK")
			dtypec = str(r"AREA:c#FFC73BFF:"+data['pitem'][2][1]+r":STACK")
			dtyped = str(r"AREA:d#74C366FF:"+data['pitem'][3][1]+r":STACK")
			dtypee = str(r"LINE1:e#000000FF:"+data['pitem'][4][1])
		else:
			dtypea = str(r"LINE1:a#862F2FFF:"+data['pitem'][0][1])
			dtypeb = str(r"LINE1:b#EA8F00FF:"+data['pitem'][1][1])
			dtypec = str(r"LINE1:c#FFC73BFF:"+data['pitem'][2][1])
			dtyped = str(r"LINE1:d#74C366FF:"+data['pitem'][3][1])
			dtypee = str(r"LINE1:e#000000FF:"+data['pitem'][4][1])
	if data['gname'] == 'Memory':
		maxa = 'GPRINT:cdefa:MAX:Max\:%.2lf %s'
		mina = 'GPRINT:cdefa:MIN:Min\:%.2lf %s'
		avga = 'GPRINT:cdefa:AVERAGE:Avg\:%.2lf %s'
		nowa = 'GPRINT:cdefa:LAST:Now\:%.2lf %s'
	else:
		maxa = 'GPRINT:a:MAX:Max\:%.2lf %s'
		mina = 'GPRINT:a:MIN:Min\:%.2lf %s'
		avga = 'GPRINT:a:AVERAGE:Avg\:%.2lf %s'
		nowa = 'GPRINT:a:LAST:Now\:%.2lf %s'
	maxb = 'GPRINT:b:MAX:Max\:%.2lf %s'
	minb = 'GPRINT:b:MIN:Min\:%.2lf %s'
	avgb = 'GPRINT:b:AVERAGE:Avg\:%.2lf %s'
	nowb = 'GPRINT:b:LAST:Now\:%.2lf %s'
	maxc = 'GPRINT:c:MAX:Max\:%.2lf %s'
	minc = 'GPRINT:c:MIN:Min\:%.2lf %s'
	avgc = 'GPRINT:c:AVERAGE:Avg\:%.2lf %s'
	nowc = 'GPRINT:c:LAST:Now\:%.2lf %s'
	maxd = 'GPRINT:d:MAX:Max\:%.2lf %s'
	mind = 'GPRINT:d:MIN:Min\:%.2lf %s'
	avgd = 'GPRINT:d:AVERAGE:Avg\:%.2lf %s'
	nowd = 'GPRINT:d:LAST:Now\:%.2lf %s'
	maxe = 'GPRINT:e:MAX:Max\:%.2lf %s'
	mine = 'GPRINT:e:MIN:Min\:%.2lf %s'
	avge = 'GPRINT:e:AVERAGE:Avg\:%.2lf %s'
	nowe = 'GPRINT:e:LAST:Now\:%.2lf %s'
	if data['gname'] == 'Memory':
		if data['flag'] == 'Daily':
			rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start, '-x', 'MINUTE:30:HOUR:2:HOUR:2:0:%H:%M',
					'-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, DEFe, cdefa, 'COMMENT: \\n', dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n', 
					dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
					dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n', dtypee, nowe, avge, mine, maxe, 'COMMENT: \\n')
		elif data['flag'] == 'Weekly':
			rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start, '-x', 'HOUR:4:HOUR:12:DAY:1:0:%d',
					'-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, DEFe, cdefa, 'COMMENT: \\n', dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n', 
					dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
					dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n', dtypee, nowe, avge, mine, maxe, 'COMMENT: \\n')
		else:
			rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start,
					'-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, DEFe, cdefa, 'COMMENT: \\n', dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n', 
					dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
					dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n', dtypee, nowe, avge, mine, maxe, 'COMMENT: \\n')
	else:
		if data['flag'] == 'Daily':
			rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start, '-x', 'MINUTE:30:HOUR:2:HOUR:2:0:%H:%M',
					'-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, DEFe, 'COMMENT: \\n', dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n', 
					dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
					dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n', dtypee, nowe, avge, mine, maxe, 'COMMENT: \\n')
		elif data['flag'] == 'Weekly':
			rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start, '-x', 'HOUR:4:HOUR:12:DAY:1:0:%d',
					'-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, DEFe, 'COMMENT: \\n', dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n', 
					dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
					dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n', dtypee, nowe, avge, mine, maxe, 'COMMENT: \\n')
		else:
			rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start,
					'-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, DEFe, 'COMMENT: \\n', dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n', 
					dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
					dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n', dtypee, nowe, avge, mine, maxe, 'COMMENT: \\n')
###################################################################################################
def dItem06(data):
	pngname = str(data['pname'])
	start = data['stime']
	graphname = str(data['gname'] + " (" + data['graphid'] + ") " + data['host'] + "(" + data['flag'] + ")")
	DEFa = str(r"DEF:a="+data['rrdpath']+r':'+data['pitem'][0][0]+r":AVERAGE")
	DEFb = str(r"DEF:b="+data['rrdpath']+r':'+data['pitem'][1][0]+r":AVERAGE")
	DEFc = str(r"DEF:c="+data['rrdpath']+r':'+data['pitem'][2][0]+r":AVERAGE")
	DEFd = str(r"DEF:d="+data['rrdpath']+r':'+data['pitem'][3][0]+r":AVERAGE")
	DEFe = str(r"DEF:e="+data['rrdpath']+r':'+data['pitem'][4][0]+r":AVERAGE")
	DEFf = str(r"DEF:f="+data['rrdpath']+r':'+data['pitem'][5][0]+r":AVERAGE")
	unit = str(data['pitem'][0][2])
	if not unit:
		unit = ' '
	if data['cols'] or data['itypes']:
		if not data['cols']:
			dtypea = str(data['itypes'][0][0]+r":a#837C04FF:"+data['pitem'][0][1])
			dtypeb = str(data['itypes'][0][1]+r":b#157419FF:"+data['pitem'][1][1])
			dtypec = str(data['itypes'][0][2]+r":c#00CF00FF:"+data['pitem'][2][1])
			dtyped = str(data['itypes'][0][3]+r":d#96E78AFF:"+data['pitem'][3][1])
			dtypee = str(data['itypes'][0][4]+r":e#00A0C1FF:"+data['pitem'][4][1])
			dtypef = str(data['itypes'][0][5]+r":f#0000FFFF:"+data['pitem'][5][1])
		elif not data['itypes']:
			dtypea = str(r"LINE1:a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
			dtypeb = str(r"LINE1:b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
			dtypec = str(r"LINE1:c"+data['cols'][0][2]+r":"+data['pitem'][2][1])
			dtyped = str(r"LINE1:d"+data['cols'][0][3]+r":"+data['pitem'][3][1])
			dtypee = str(r"LINE1:e"+data['cols'][0][4]+r":"+data['pitem'][4][1])
			dtypef = str(r"LINE1:f"+data['cols'][0][5]+r":"+data['pitem'][5][1])
		else:
			dtypea = str(data['itypes'][0][0]+r":a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
			dtypeb = str(data['itypes'][0][1]+r":b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
			dtypec = str(data['itypes'][0][2]+r":c"+data['cols'][0][2]+r":"+data['pitem'][2][1])
			dtyped = str(data['itypes'][0][3]+r":d"+data['cols'][0][3]+r":"+data['pitem'][3][1])
			dtypee = str(data['itypes'][0][4]+r":e"+data['cols'][0][4]+r":"+data['pitem'][4][1])
			dtypef = str(data['itypes'][0][5]+r":f"+data['cols'][0][5]+r":"+data['pitem'][5][1])
	else:
		dtypea = str(r"LINE1:a#837C04FF:"+data['pitem'][0][1])
		dtypeb = str(r"LINE1:b#157419FF:"+data['pitem'][1][1])
		dtypec = str(r"LINE1:c#00CF00FF:"+data['pitem'][2][1])
		dtyped = str(r"LINE1:d#96E78AFF:"+data['pitem'][3][1])
		dtypee = str(r"LINE1:e#00A0C1FF:"+data['pitem'][4][1])
		dtypef = str(r"LINE1:f#0000FFFF:"+data['pitem'][5][1])
	maxa = 'GPRINT:a:MAX:Max\:%.2lf %s'
	mina = 'GPRINT:a:MIN:Min\:%.2lf %s'
	avga = 'GPRINT:a:AVERAGE:Avg\:%.2lf %s'
	nowa = 'GPRINT:a:LAST:Now\:%.2lf %s'
	maxb = 'GPRINT:b:MAX:Max\:%.2lf %s'
	minb = 'GPRINT:b:MIN:Min\:%.2lf %s'
	avgb = 'GPRINT:b:AVERAGE:Avg\:%.2lf %s'
	nowb = 'GPRINT:b:LAST:Now\:%.2lf %s'
	maxc = 'GPRINT:c:MAX:Max\:%.2lf %s'
	minc = 'GPRINT:c:MIN:Min\:%.2lf %s'
	avgc = 'GPRINT:c:AVERAGE:Avg\:%.2lf %s'
	nowc = 'GPRINT:c:LAST:Now\:%.2lf %s'
	maxd = 'GPRINT:d:MAX:Max\:%.2lf %s'
	mind = 'GPRINT:d:MIN:Min\:%.2lf %s'
	avgd = 'GPRINT:d:AVERAGE:Avg\:%.2lf %s'
	nowd = 'GPRINT:d:LAST:Now\:%.2lf %s'
	maxe = 'GPRINT:e:MAX:Max\:%.2lf %s'
	mine = 'GPRINT:e:MIN:Min\:%.2lf %s'
	avge = 'GPRINT:e:AVERAGE:Avg\:%.2lf %s'
	nowe = 'GPRINT:e:LAST:Now\:%.2lf %s'
	maxf = 'GPRINT:f:MAX:Max\:%.2lf %s'
	minf = 'GPRINT:f:MIN:Min\:%.2lf %s'
	avgf = 'GPRINT:f:AVERAGE:Avg\:%.2lf %s'
	nowf = 'GPRINT:f:LAST:Now\:%.2lf %s'
	if data['flag'] == 'Daily':
		rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start, '-x', 'MINUTE:30:HOUR:2:HOUR:2:0:%H:%M',
					'-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, DEFe, DEFf, 'COMMENT: \\n', dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n', 
					dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
					dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n', dtypee, nowe, avge, mine, maxe, 'COMMENT: \\n', 
					dtypef, nowf, avgf, minf, maxf, 'COMMENT: \\n')
	elif data['flag'] == 'Weekly':
		rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start, '-x', 'HOUR:4:HOUR:12:DAY:1:0:%d',
					'-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, DEFe, DEFf, 'COMMENT: \\n', dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n', 
					dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
					dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n', dtypee, nowe, avge, mine, maxe, 'COMMENT: \\n', 
					dtypef, nowf, avgf, minf, maxf, 'COMMENT: \\n')
	else:
		rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start,
					'-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, DEFe, DEFf, 'COMMENT: \\n', dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n', 
					dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
					dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n', dtypee, nowe, avge, mine, maxe, 'COMMENT: \\n', 
					dtypef, nowf, avgf, minf, maxf, 'COMMENT: \\n')

def dItem08(data):
	pngname = str(data['pname'])
	start = data['stime']
	graphname = str(data['gname'] + " (" + data['graphid'] + ") " + data['host'] + "(" + data['flag'] + ")")
	DEFa = str(r"DEF:a="+data['rrdpath']+r':'+data['pitem'][0][0]+r":AVERAGE")
	DEFb = str(r"DEF:b="+data['rrdpath']+r':'+data['pitem'][1][0]+r":AVERAGE")
	DEFc = str(r"DEF:c="+data['rrdpath']+r':'+data['pitem'][2][0]+r":AVERAGE")
	DEFd = str(r"DEF:d="+data['rrdpath']+r':'+data['pitem'][3][0]+r":AVERAGE")
	DEFe = str(r"DEF:e="+data['rrdpath']+r':'+data['pitem'][4][0]+r":AVERAGE")
	DEFf = str(r"DEF:f="+data['rrdpath']+r':'+data['pitem'][5][0]+r":AVERAGE")
	DEFg = str(r"DEF:g="+data['rrdpath']+r':'+data['pitem'][6][0]+r":AVERAGE")
	DEFh = str(r"DEF:h="+data['rrdpath']+r':'+data['pitem'][7][0]+r":AVERAGE")
	unit = str(data['pitem'][0][2])
	if not unit:
		unit = ' '
	if data['cols'] or data['itypes']:
		if not data['cols']:
			dtypea = str(data['itypes'][0][0]+r":a#FF0000FF:"+data['pitem'][0][1])
			dtypeb = str(data['itypes'][0][1]+r":b#000000FF:"+data['pitem'][1][1])
			dtypec = str(data['itypes'][0][2]+r":c#00FF00FF:"+data['pitem'][2][1])
			dtyped = str(data['itypes'][0][3]+r":d#F5F800FF:"+data['pitem'][3][1])
			dtypee = str(data['itypes'][0][4]+r":e#00BED9FF:"+data['pitem'][4][1])
			dtypef = str(data['itypes'][0][4]+r":f#4668E4FF:"+data['pitem'][5][1])
			dtypeg = str(data['itypes'][0][6]+r":g#0000FFFF:"+data['pitem'][6][1])
			dtypeh = str(data['itypes'][0][7]+r":h#FF00FFFF:"+data['pitem'][7][1])
		elif not data['itypes']:
			dtypea = str(r"LINE1:a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
			dtypeb = str(r"LINE1:b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
			dtypec = str(r"LINE1:c"+data['cols'][0][2]+r":"+data['pitem'][2][1])
			dtyped = str(r"LINE1:d"+data['cols'][0][3]+r":"+data['pitem'][3][1])
			dtypee = str(r"LINE1:e"+data['cols'][0][4]+r":"+data['pitem'][4][1])
			dtypef = str(r"LINE1:f"+data['cols'][0][5]+r":"+data['pitem'][5][1])
			dtypeg = str(r"LINE1:g"+data['cols'][0][6]+r":"+data['pitem'][6][1])
			dtypeh = str(r"LINE1:h"+data['cols'][0][7]+r":"+data['pitem'][7][1])
		else:
			dtypea = str(data['itypes'][0][0]+r":a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
			dtypeb = str(data['itypes'][0][1]+r":b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
			dtypec = str(data['itypes'][0][2]+r":c"+data['cols'][0][2]+r":"+data['pitem'][2][1])
			dtyped = str(data['itypes'][0][3]+r":d"+data['cols'][0][3]+r":"+data['pitem'][3][1])
			dtypee = str(data['itypes'][0][4]+r":e"+data['cols'][0][4]+r":"+data['pitem'][4][1])
			dtypef = str(data['itypes'][0][5]+r":f"+data['cols'][0][5]+r":"+data['pitem'][5][1])
			dtypeg = str(data['itypes'][0][6]+r":g"+data['cols'][0][6]+r":"+data['pitem'][6][1])
			dtypeh = str(data['itypes'][0][7]+r":h"+data['cols'][0][7]+r":"+data['pitem'][7][1])
	else:
		if data['gname'] == 'CPU utilization':
			dtypea = str(r"AREA:a#FF0000FF:"+data['pitem'][0][1]+r":STACK")
			dtypeb = str(r"AREA:b#F5F800FF:"+data['pitem'][1][1]+r":STACK")
			dtypec = str(r"AREA:c#00FF00FF:"+data['pitem'][2][1]+r":STACK")
			dtyped = str(r"LINE1:d#000000FF:"+data['pitem'][3][1])
			dtypee = str(r"AREA:e#00BED9FF:"+data['pitem'][4][1]+r":STACK")
			dtypef = str(r"AREA:f#4668E4FF:"+data['pitem'][5][1]+r":STACK")
			dtypeg = str(r"AREA:g#0000FFFF:"+data['pitem'][6][1]+r":STACK")
			dtypeh = str(r"AREA:h#FF00FFFF:"+data['pitem'][7][1]+r":STACK")
		else:
			dtypea = str(r"LINE1:a#FF0000FF:"+data['pitem'][0][1])
			dtypeb = str(r"LINE1:b#000000FF:"+data['pitem'][1][1])
			dtypec = str(r"LINE1:c#00FF00FF:"+data['pitem'][2][1])
			dtyped = str(r"LINE1:d#F5F800FF:"+data['pitem'][3][1])
			dtypee = str(r"LINE1:e#00BED9FF:"+data['pitem'][4][1])
			dtypef = str(r"LINE1:f#4668E4FF:"+data['pitem'][5][1])
			dtypeg = str(r"LINE1:g#0000FFFF:"+data['pitem'][6][1])
			dtypeh = str(r"LINE1:h#FF00FFFF:"+data['pitem'][7][1])
	maxa = 'GPRINT:a:MAX:Max\:%.2lf %s'
	mina = 'GPRINT:a:MIN:Min\:%.2lf %s'
	avga = 'GPRINT:a:AVERAGE:Avg\:%.2lf %s'
	nowa = 'GPRINT:a:LAST:Now\:%.2lf %s'
	maxb = 'GPRINT:b:MAX:Max\:%.2lf %s'
	minb = 'GPRINT:b:MIN:Min\:%.2lf %s'
	avgb = 'GPRINT:b:AVERAGE:Avg\:%.2lf %s'
	nowb = 'GPRINT:b:LAST:Now\:%.2lf %s'
	maxc = 'GPRINT:c:MAX:Max\:%.2lf %s'
	minc = 'GPRINT:c:MIN:Min\:%.2lf %s'
	avgc = 'GPRINT:c:AVERAGE:Avg\:%.2lf %s'
	nowc = 'GPRINT:c:LAST:Now\:%.2lf %s'
	maxd = 'GPRINT:d:MAX:Max\:%.2lf %s'
	mind = 'GPRINT:d:MIN:Min\:%.2lf %s'
	avgd = 'GPRINT:d:AVERAGE:Avg\:%.2lf %s'
	nowd = 'GPRINT:d:LAST:Now\:%.2lf %s'
	maxe = 'GPRINT:e:MAX:Max\:%.2lf %s'
	mine = 'GPRINT:e:MIN:Min\:%.2lf %s'
	avge = 'GPRINT:e:AVERAGE:Avg\:%.2lf %s'
	nowe = 'GPRINT:e:LAST:Now\:%.2lf %s'
	maxf = 'GPRINT:f:MAX:Max\:%.2lf %s'
	minf = 'GPRINT:f:MIN:Min\:%.2lf %s'
	avgf = 'GPRINT:f:AVERAGE:Avg\:%.2lf %s'
	nowf = 'GPRINT:f:LAST:Now\:%.2lf %s'
	maxg = 'GPRINT:g:MAX:Max\:%.2lf %s'
	ming = 'GPRINT:g:MIN:Min\:%.2lf %s'
	avgg = 'GPRINT:g:AVERAGE:Avg\:%.2lf %s'
	nowg = 'GPRINT:g:LAST:Now\:%.2lf %s'
	maxh = 'GPRINT:h:MAX:Max\:%.2lf %s'
	minh = 'GPRINT:h:MIN:Min\:%.2lf %s'
	avgh = 'GPRINT:h:AVERAGE:Avg\:%.2lf %s'
	nowh = 'GPRINT:h:LAST:Now\:%.2lf %s'
	if data['flag'] == 'Daily':
		rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start, '-x', 'MINUTE:30:HOUR:2:HOUR:2:0:%H:%M',
					'-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, DEFe, DEFf, DEFg, DEFh, 'COMMENT: \\n', dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n',
					dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
					dtypeh, nowh, avgh, minh, maxh, 'COMMENT: \\n', dtypee, nowe, avge, mine, maxe, 'COMMENT: \\n',
					dtypef, nowf, avgf, minf, maxf, 'COMMENT: \\n',	dtypeg, nowg, avgg, ming, maxg, 'COMMENT: \\n',
					dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n')
	elif data['flag'] == 'Weekly':
		rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start, '-x', 'HOUR:4:HOUR:12:DAY:1:0:%d',
					'-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, DEFe, DEFf, DEFg, DEFh, 'COMMENT: \\n', dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n',
					dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
					dtypeh, nowh, avgh, minh, maxh, 'COMMENT: \\n', dtypee, nowe, avge, mine, maxe, 'COMMENT: \\n',
					dtypef, nowf, avgf, minf, maxf, 'COMMENT: \\n',	dtypeg, nowg, avgg, ming, maxg, 'COMMENT: \\n',
					dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n')
	else:
		rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start,
					'-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, DEFe, DEFf, DEFg, DEFh, 'COMMENT: \\n', dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n',
					dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
					dtypeh, nowh, avgh, minh, maxh, 'COMMENT: \\n', dtypee, nowe, avge, mine, maxe, 'COMMENT: \\n',
					dtypef, nowf, avgf, minf, maxf, 'COMMENT: \\n',	dtypeg, nowg, avgg, ming, maxg, 'COMMENT: \\n',
					dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n')

def dItem11(data):
	pngname = str(data['pname'])
	start = data['stime']
	graphname = str(data['gname'] + " (" + data['graphid'] + ") " + data['host'] + "(" + data['flag'] + ")")
	DEFa = str(r"DEF:a="+data['rrdpath']+r':'+data['pitem'][0][0]+r":AVERAGE")
	DEFb = str(r"DEF:b="+data['rrdpath']+r':'+data['pitem'][1][0]+r":AVERAGE")
	DEFc = str(r"DEF:c="+data['rrdpath']+r':'+data['pitem'][2][0]+r":AVERAGE")
	DEFd = str(r"DEF:d="+data['rrdpath']+r':'+data['pitem'][3][0]+r":AVERAGE")
	DEFe = str(r"DEF:e="+data['rrdpath']+r':'+data['pitem'][4][0]+r":AVERAGE")
	DEFf = str(r"DEF:f="+data['rrdpath']+r':'+data['pitem'][5][0]+r":AVERAGE")
	DEFg = str(r"DEF:g="+data['rrdpath']+r':'+data['pitem'][6][0]+r":AVERAGE")
	DEFh = str(r"DEF:h="+data['rrdpath']+r':'+data['pitem'][7][0]+r":AVERAGE")
	DEFi = str(r"DEF:i="+data['rrdpath']+r':'+data['pitem'][8][0]+r":AVERAGE")
	DEFj = str(r"DEF:j="+data['rrdpath']+r':'+data['pitem'][9][0]+r":AVERAGE")
	DEFk = str(r"DEF:k="+data['rrdpath']+r':'+data['pitem'][10][0]+r":AVERAGE")
	unit = str(data['pitem'][0][2])
	if not unit:
		unit = ' '
	if data['cols'] or data['itypes']:
		if not data['cols']:
			dtypea = str(data['itypes'][0][0]+r":a#837C04FF:"+data['pitem'][0][1])
			dtypeb = str(data['itypes'][0][1]+r":b#8F9286FF:"+data['pitem'][1][1])
			dtypec = str(data['itypes'][0][2]+r":c#562B29FF:"+data['pitem'][2][1])
			dtyped = str(data['itypes'][0][3]+r":d#AFECEDFF:"+data['pitem'][3][1])
			dtypee = str(data['itypes'][0][4]+r":e#D8ACE0FF:"+data['pitem'][4][1])
			dtypef = str(data['itypes'][0][4]+r":f#ED7600FF:"+data['pitem'][5][1])
			dtypeg = str(data['itypes'][0][6]+r":g#FF00FFFF:"+data['pitem'][6][1])
			dtypeh = str(data['itypes'][0][7]+r":h#FFC73BFF:"+data['pitem'][7][1])
			dtypei = str(data['itypes'][0][8]+r":i#837C04FF:"+data['pitem'][8][1])
			dtypej = str(data['itypes'][0][9]+r":j#157419FF:"+data['pitem'][9][1])
			dtypek = str(data['itypes'][0][10]+r":k#00CF00FF:"+data['pitem'][10][1])
		elif not data['itypes']:
			dtypea = str(r"LINE1:a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
			dtypeb = str(r"LINE1:b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
			dtypec = str(r"LINE1:c"+data['cols'][0][2]+r":"+data['pitem'][2][1])
			dtyped = str(r"LINE1:d"+data['cols'][0][3]+r":"+data['pitem'][3][1])
			dtypee = str(r"LINE1:e"+data['cols'][0][4]+r":"+data['pitem'][4][1])
			dtypef = str(r"LINE1:f"+data['cols'][0][5]+r":"+data['pitem'][5][1])
			dtypeg = str(r"LINE1:g"+data['cols'][0][6]+r":"+data['pitem'][6][1])
			dtypeh = str(r"LINE1:h"+data['cols'][0][7]+r":"+data['pitem'][7][1])
			dtypei = str(r"LINE1:i"+data['cols'][0][8]+r":"+data['pitem'][8][1])
			dtypej = str(r"LINE1:j"+data['cols'][0][9]+r":"+data['pitem'][9][1])
			dtypek = str(r"LINE1:k"+data['cols'][0][10]+r":"+data['pitem'][10][1])
		else:
			dtypea = str(data['itypes'][0][0]+r":a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
			dtypeb = str(data['itypes'][0][1]+r":b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
			dtypec = str(data['itypes'][0][2]+r":c"+data['cols'][0][2]+r":"+data['pitem'][2][1])
			dtyped = str(data['itypes'][0][3]+r":d"+data['cols'][0][3]+r":"+data['pitem'][3][1])
			dtypee = str(data['itypes'][0][4]+r":e"+data['cols'][0][4]+r":"+data['pitem'][4][1])
			dtypef = str(data['itypes'][0][5]+r":f"+data['cols'][0][5]+r":"+data['pitem'][5][1])
			dtypeg = str(data['itypes'][0][6]+r":g"+data['cols'][0][6]+r":"+data['pitem'][6][1])
			dtypeh = str(data['itypes'][0][7]+r":h"+data['cols'][0][7]+r":"+data['pitem'][7][1])
			dtypei = str(data['itypes'][0][8]+r":i"+data['cols'][0][8]+r":"+data['pitem'][8][1])
			dtypej = str(data['itypes'][0][9]+r":j"+data['cols'][0][9]+r":"+data['pitem'][9][1])
			dtypek = str(data['itypes'][0][10]+r":k"+data['cols'][0][10]+r":"+data['pitem'][10][1])
	else:
		dtypea = str(r"LINE1:a#837C04FF:"+data['pitem'][0][1])
		dtypeb = str(r"LINE1:b#8F9286FF:"+data['pitem'][1][1])
		dtypec = str(r"LINE1:c#562B29FF:"+data['pitem'][2][1])
		dtyped = str(r"LINE1:d#AFECEDFF:"+data['pitem'][3][1])
		dtypee = str(r"LINE1:e#D8ACE0FF:"+data['pitem'][4][1])
		dtypef = str(r"LINE1:f#ED7600FF:"+data['pitem'][5][1])
		dtypeg = str(r"LINE1:g#FF00FFFF:"+data['pitem'][6][1])
		dtypeh = str(r"LINE1:h#FFC73BFF:"+data['pitem'][7][1])
		dtypei = str(r"LINE1:i#837C04FF:"+data['pitem'][8][1])
		dtypej = str(r"LINE1:j#157419FF:"+data['pitem'][9][1])
		dtypek = str(r"LINE1:k#00CF00FF:"+data['pitem'][10][1])
	maxa = 'GPRINT:a:MAX:Max\:%.2lf %s'
	mina = 'GPRINT:a:MIN:Min\:%.2lf %s'
	avga = 'GPRINT:a:AVERAGE:Avg\:%.2lf %s'
	nowa = 'GPRINT:a:LAST:Now\:%.2lf %s'
	maxb = 'GPRINT:b:MAX:Max\:%.2lf %s'
	minb = 'GPRINT:b:MIN:Min\:%.2lf %s'
	avgb = 'GPRINT:b:AVERAGE:Avg\:%.2lf %s'
	nowb = 'GPRINT:b:LAST:Now\:%.2lf %s'
	maxc = 'GPRINT:c:MAX:Max\:%.2lf %s'
	minc = 'GPRINT:c:MIN:Min\:%.2lf %s'
	avgc = 'GPRINT:c:AVERAGE:Avg\:%.2lf %s'
	nowc = 'GPRINT:c:LAST:Now\:%.2lf %s'
	maxd = 'GPRINT:d:MAX:Max\:%.2lf %s'
	mind = 'GPRINT:d:MIN:Min\:%.2lf %s'
	avgd = 'GPRINT:d:AVERAGE:Avg\:%.2lf %s'
	nowd = 'GPRINT:d:LAST:Now\:%.2lf %s'
	maxe = 'GPRINT:e:MAX:Max\:%.2lf %s'
	mine = 'GPRINT:e:MIN:Min\:%.2lf %s'
	avge = 'GPRINT:e:AVERAGE:Avg\:%.2lf %s'
	nowe = 'GPRINT:e:LAST:Now\:%.2lf %s'
	maxf = 'GPRINT:f:MAX:Max\:%.2lf %s'
	minf = 'GPRINT:f:MIN:Min\:%.2lf %s'
	avgf = 'GPRINT:f:AVERAGE:Avg\:%.2lf %s'
	nowf = 'GPRINT:f:LAST:Now\:%.2lf %s'
	maxg = 'GPRINT:g:MAX:Max\:%.2lf %s'
	ming = 'GPRINT:g:MIN:Min\:%.2lf %s'
	avgg = 'GPRINT:g:AVERAGE:Avg\:%.2lf %s'
	nowg = 'GPRINT:g:LAST:Now\:%.2lf %s'
	maxh = 'GPRINT:h:MAX:Max\:%.2lf %s'
	minh = 'GPRINT:h:MIN:Min\:%.2lf %s'
	avgh = 'GPRINT:h:AVERAGE:Avg\:%.2lf %s'
	nowh = 'GPRINT:h:LAST:Now\:%.2lf %s'
	maxi = 'GPRINT:i:MAX:Max\:%.2lf %s'
	mini = 'GPRINT:i:MIN:Min\:%.2lf %s'
	avgi = 'GPRINT:i:AVERAGE:Avg\:%.2lf %s'
	nowi = 'GPRINT:i:LAST:Now\:%.2lf %s'
	maxj = 'GPRINT:j:MAX:Max\:%.2lf %s'
	minj = 'GPRINT:j:MIN:Min\:%.2lf %s'
	avgj = 'GPRINT:j:AVERAGE:Avg\:%.2lf %s'
	nowj = 'GPRINT:j:LAST:Now\:%.2lf %s'
	maxk = 'GPRINT:k:MAX:Max\:%.2lf %s'
	mink = 'GPRINT:k:MIN:Min\:%.2lf %s'
	avgk = 'GPRINT:k:AVERAGE:Avg\:%.2lf %s'
	nowk = 'GPRINT:k:LAST:Now\:%.2lf %s'
	if data['flag'] == 'Daily':
		rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start, '-x', 'MINUTE:30:HOUR:2:HOUR:2:0:%H:%M',
					'-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, DEFe, DEFf, DEFg, DEFh, DEFi, DEFj, DEFk, 'COMMENT: \\n', 
					dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n', dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
					dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n', dtypee, nowe, avge, mine, maxe, 'COMMENT: \\n', dtypef, nowf, avgf, minf, maxf, 'COMMENT: \\n',	
					dtypeg, nowg, avgg, ming, maxg, 'COMMENT: \\n',	dtypeh, nowh, avgh, minh, maxh, 'COMMENT: \\n',	dtypei, nowi, avgi, mini, maxi, 'COMMENT: \\n',	
					dtypej, nowj, avgj, minj, maxj, 'COMMENT: \\n',	dtypek, nowk, avgk, mink, maxk, 'COMMENT: \\n')
	elif data['flag'] == 'Weekly':
		rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start, '-x', 'HOUR:4:HOUR:12:DAY:1:0:%d',
					'-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, DEFe, DEFf, DEFg, DEFh, DEFi, DEFj, DEFk, 'COMMENT: \\n', 
					dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n', dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
					dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n', dtypee, nowe, avge, mine, maxe, 'COMMENT: \\n', dtypef, nowf, avgf, minf, maxf, 'COMMENT: \\n',	
					dtypeg, nowg, avgg, ming, maxg, 'COMMENT: \\n',	dtypeh, nowh, avgh, minh, maxh, 'COMMENT: \\n',	dtypei, nowi, avgi, mini, maxi, 'COMMENT: \\n',	
					dtypej, nowj, avgj, minj, maxj, 'COMMENT: \\n',	dtypek, nowk, avgk, mink, maxk, 'COMMENT: \\n')
	else:
		rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start,
					'-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, DEFe, DEFf, DEFg, DEFh, DEFi, DEFj, DEFk, 'COMMENT: \\n', 
					dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n', dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
					dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n', dtypee, nowe, avge, mine, maxe, 'COMMENT: \\n', dtypef, nowf, avgf, minf, maxf, 'COMMENT: \\n',	
					dtypeg, nowg, avgg, ming, maxg, 'COMMENT: \\n',	dtypeh, nowh, avgh, minh, maxh, 'COMMENT: \\n',	dtypei, nowi, avgi, mini, maxi, 'COMMENT: \\n',	
					dtypej, nowj, avgj, minj, maxj, 'COMMENT: \\n',	dtypek, nowk, avgk, mink, maxk, 'COMMENT: \\n')
#######################################################################################
def dItem12(data):
	pngname = str(data['pname'])
	start = data['stime']
	graphname = str(data['gname'] + " (" + data['graphid'] + ") " + data['host'] + "(" + data['flag'] + ")")
	DEFa = str(r"DEF:a="+data['rrdpath']+r':'+data['pitem'][0][0]+r":AVERAGE")
	DEFb = str(r"DEF:b="+data['rrdpath']+r':'+data['pitem'][1][0]+r":AVERAGE")
	DEFc = str(r"DEF:c="+data['rrdpath']+r':'+data['pitem'][2][0]+r":AVERAGE")
	DEFd = str(r"DEF:d="+data['rrdpath']+r':'+data['pitem'][3][0]+r":AVERAGE")
	DEFe = str(r"DEF:e="+data['rrdpath']+r':'+data['pitem'][4][0]+r":AVERAGE")
	DEFf = str(r"DEF:f="+data['rrdpath']+r':'+data['pitem'][5][0]+r":AVERAGE")
	DEFg = str(r"DEF:g="+data['rrdpath']+r':'+data['pitem'][6][0]+r":AVERAGE")
	DEFh = str(r"DEF:h="+data['rrdpath']+r':'+data['pitem'][7][0]+r":AVERAGE")
	DEFi = str(r"DEF:i="+data['rrdpath']+r':'+data['pitem'][8][0]+r":AVERAGE")
	DEFj = str(r"DEF:j="+data['rrdpath']+r':'+data['pitem'][9][0]+r":AVERAGE")
	DEFk = str(r"DEF:k="+data['rrdpath']+r':'+data['pitem'][10][0]+r":AVERAGE")
	DEFl = str(r"DEF:l="+data['rrdpath']+r':'+data['pitem'][11][0]+r":AVERAGE")
	unit = str(data['pitem'][0][2])
	if not unit:
		unit = ' '
	if data['cols'] or data['itypes']:
		if not data['cols']:
			dtypea = str(data['itypes'][0][0]+r":a#837C04FF:"+data['pitem'][0][1])
			dtypeb = str(data['itypes'][0][1]+r":b#8F9286FF:"+data['pitem'][1][1])
			dtypec = str(data['itypes'][0][2]+r":c#562B29FF:"+data['pitem'][2][1])
			dtyped = str(data['itypes'][0][3]+r":d#AFECEDFF:"+data['pitem'][3][1])
			dtypee = str(data['itypes'][0][4]+r":e#D8ACE0FF:"+data['pitem'][4][1])
			dtypef = str(data['itypes'][0][4]+r":f#ED7600FF:"+data['pitem'][5][1])
			dtypeg = str(data['itypes'][0][6]+r":g#FF00FFFF:"+data['pitem'][6][1])
			dtypeh = str(data['itypes'][0][7]+r":h#FFC73BFF:"+data['pitem'][7][1])
			dtypei = str(data['itypes'][0][8]+r":i#837C04FF:"+data['pitem'][8][1])
			dtypej = str(data['itypes'][0][9]+r":j#157419FF:"+data['pitem'][9][1])
			dtypek = str(data['itypes'][0][10]+r":k#00CF00FF:"+data['pitem'][10][1])
			dtypel = str(data['itypes'][0][11]+r":l#FF0000FF:"+data['pitem'][11][1])
		elif not data['itypes']:
			dtypea = str(r"LINE1:a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
			dtypeb = str(r"LINE1:b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
			dtypec = str(r"LINE1:c"+data['cols'][0][2]+r":"+data['pitem'][2][1])
			dtyped = str(r"LINE1:d"+data['cols'][0][3]+r":"+data['pitem'][3][1])
			dtypee = str(r"LINE1:e"+data['cols'][0][4]+r":"+data['pitem'][4][1])
			dtypef = str(r"LINE1:f"+data['cols'][0][5]+r":"+data['pitem'][5][1])
			dtypeg = str(r"LINE1:g"+data['cols'][0][6]+r":"+data['pitem'][6][1])
			dtypeh = str(r"LINE1:h"+data['cols'][0][7]+r":"+data['pitem'][7][1])
			dtypei = str(r"LINE1:i"+data['cols'][0][8]+r":"+data['pitem'][8][1])
			dtypej = str(r"LINE1:j"+data['cols'][0][9]+r":"+data['pitem'][9][1])
			dtypek = str(r"LINE1:k"+data['cols'][0][10]+r":"+data['pitem'][10][1])
			dtypel = str(r"LINE1:l"+data['cols'][0][11]+r":"+data['pitem'][11][1])
		else:
			dtypea = str(data['itypes'][0][0]+r":a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
			dtypeb = str(data['itypes'][0][1]+r":b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
			dtypec = str(data['itypes'][0][2]+r":c"+data['cols'][0][2]+r":"+data['pitem'][2][1])
			dtyped = str(data['itypes'][0][3]+r":d"+data['cols'][0][3]+r":"+data['pitem'][3][1])
			dtypee = str(data['itypes'][0][4]+r":e"+data['cols'][0][4]+r":"+data['pitem'][4][1])
			dtypef = str(data['itypes'][0][5]+r":f"+data['cols'][0][5]+r":"+data['pitem'][5][1])
			dtypeg = str(data['itypes'][0][6]+r":g"+data['cols'][0][6]+r":"+data['pitem'][6][1])
			dtypeh = str(data['itypes'][0][7]+r":h"+data['cols'][0][7]+r":"+data['pitem'][7][1])
			dtypei = str(data['itypes'][0][8]+r":i"+data['cols'][0][8]+r":"+data['pitem'][8][1])
			dtypej = str(data['itypes'][0][9]+r":j"+data['cols'][0][9]+r":"+data['pitem'][9][1])
			dtypek = str(data['itypes'][0][10]+r":k"+data['cols'][0][10]+r":"+data['pitem'][10][1])
			dtypel = str(data['itypes'][0][11]+r":l"+data['cols'][0][11]+r":"+data['pitem'][11][1])
	else:
		dtypea = str(r"LINE1:a#837C04FF:"+data['pitem'][0][1])
		dtypeb = str(r"LINE1:b#8F9286FF:"+data['pitem'][1][1])
		dtypec = str(r"LINE1:c#562B29FF:"+data['pitem'][2][1])
		dtyped = str(r"LINE1:d#AFECEDFF:"+data['pitem'][3][1])
		dtypee = str(r"LINE1:e#D8ACE0FF:"+data['pitem'][4][1])
		dtypef = str(r"LINE1:f#ED7600FF:"+data['pitem'][5][1])
		dtypeg = str(r"LINE1:g#FF00FFFF:"+data['pitem'][6][1])
		dtypeh = str(r"LINE1:h#FFC73BFF:"+data['pitem'][7][1])
		dtypei = str(r"LINE1:i#837C04FF:"+data['pitem'][8][1])
		dtypej = str(r"LINE1:j#157419FF:"+data['pitem'][9][1])
		dtypek = str(r"LINE1:k#00CF00FF:"+data['pitem'][10][1])
		dtypel = str(r"LINE1:l#FF0000FF:"+data['pitem'][11][1])
	maxa = 'GPRINT:a:MAX:Max\:%.2lf %s'
	mina = 'GPRINT:a:MIN:Min\:%.2lf %s'
	avga = 'GPRINT:a:AVERAGE:Avg\:%.2lf %s'
	nowa = 'GPRINT:a:LAST:Now\:%.2lf %s'
	maxb = 'GPRINT:b:MAX:Max\:%.2lf %s'
	minb = 'GPRINT:b:MIN:Min\:%.2lf %s'
	avgb = 'GPRINT:b:AVERAGE:Avg\:%.2lf %s'
	nowb = 'GPRINT:b:LAST:Now\:%.2lf %s'
	maxc = 'GPRINT:c:MAX:Max\:%.2lf %s'
	minc = 'GPRINT:c:MIN:Min\:%.2lf %s'
	avgc = 'GPRINT:c:AVERAGE:Avg\:%.2lf %s'
	nowc = 'GPRINT:c:LAST:Now\:%.2lf %s'
	maxd = 'GPRINT:d:MAX:Max\:%.2lf %s'
	mind = 'GPRINT:d:MIN:Min\:%.2lf %s'
	avgd = 'GPRINT:d:AVERAGE:Avg\:%.2lf %s'
	nowd = 'GPRINT:d:LAST:Now\:%.2lf %s'
	maxe = 'GPRINT:e:MAX:Max\:%.2lf %s'
	mine = 'GPRINT:e:MIN:Min\:%.2lf %s'
	avge = 'GPRINT:e:AVERAGE:Avg\:%.2lf %s'
	nowe = 'GPRINT:e:LAST:Now\:%.2lf %s'
	maxf = 'GPRINT:f:MAX:Max\:%.2lf %s'
	minf = 'GPRINT:f:MIN:Min\:%.2lf %s'
	avgf = 'GPRINT:f:AVERAGE:Avg\:%.2lf %s'
	nowf = 'GPRINT:f:LAST:Now\:%.2lf %s'
	maxg = 'GPRINT:g:MAX:Max\:%.2lf %s'
	ming = 'GPRINT:g:MIN:Min\:%.2lf %s'
	avgg = 'GPRINT:g:AVERAGE:Avg\:%.2lf %s'
	nowg = 'GPRINT:g:LAST:Now\:%.2lf %s'
	maxh = 'GPRINT:h:MAX:Max\:%.2lf %s'
	minh = 'GPRINT:h:MIN:Min\:%.2lf %s'
	avgh = 'GPRINT:h:AVERAGE:Avg\:%.2lf %s'
	nowh = 'GPRINT:h:LAST:Now\:%.2lf %s'
	maxi = 'GPRINT:i:MAX:Max\:%.2lf %s'
	mini = 'GPRINT:i:MIN:Min\:%.2lf %s'
	avgi = 'GPRINT:i:AVERAGE:Avg\:%.2lf %s'
	nowi = 'GPRINT:i:LAST:Now\:%.2lf %s'
	maxj = 'GPRINT:j:MAX:Max\:%.2lf %s'
	minj = 'GPRINT:j:MIN:Min\:%.2lf %s'
	avgj = 'GPRINT:j:AVERAGE:Avg\:%.2lf %s'
	nowj = 'GPRINT:j:LAST:Now\:%.2lf %s'
	maxk = 'GPRINT:k:MAX:Max\:%.2lf %s'
	mink = 'GPRINT:k:MIN:Min\:%.2lf %s'
	avgk = 'GPRINT:k:AVERAGE:Avg\:%.2lf %s'
	nowk = 'GPRINT:k:LAST:Now\:%.2lf %s'
	maxl = 'GPRINT:l:MAX:Max\:%.2lf %s'
	minl = 'GPRINT:l:MIN:Min\:%.2lf %s'
	avgl = 'GPRINT:l:AVERAGE:Avg\:%.2lf %s'
	nowl = 'GPRINT:l:LAST:Now\:%.2lf %s'
	if data['flag'] == 'Daily':
		rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start, '-x', 'MINUTE:30:HOUR:2:HOUR:2:0:%H:%M',
					'-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, DEFe, DEFf, DEFg, DEFh, DEFi, DEFj, DEFk, DEFl, 'COMMENT: \\n', 
					dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n', dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
					dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n', dtypee, nowe, avge, mine, maxe, 'COMMENT: \\n',	dtypef, nowf, avgf, minf, maxf, 'COMMENT: \\n',	
					dtypeg, nowg, avgg, ming, maxg, 'COMMENT: \\n',	dtypeh, nowh, avgh, minh, maxh, 'COMMENT: \\n',	dtypei, nowi, avgi, mini, maxi, 'COMMENT: \\n',	
					dtypej, nowj, avgj, minj, maxj, 'COMMENT: \\n',	dtypek, nowk, avgk, mink, maxk, 'COMMENT: \\n',	dtypel, nowl, avgl, minl, maxl, 'COMMENT: \\n')
	elif data['flag'] == 'Weekly':
		rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start, '-x', 'HOUR:4:HOUR:12:DAY:1:0:%d',
					'-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, DEFe, DEFf, DEFg, DEFh, DEFi, DEFj, DEFk, DEFl, 'COMMENT: \\n', 
					dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n', dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
					dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n', dtypee, nowe, avge, mine, maxe, 'COMMENT: \\n',	dtypef, nowf, avgf, minf, maxf, 'COMMENT: \\n',	
					dtypeg, nowg, avgg, ming, maxg, 'COMMENT: \\n',	dtypeh, nowh, avgh, minh, maxh, 'COMMENT: \\n',	dtypei, nowi, avgi, mini, maxi, 'COMMENT: \\n',	
					dtypej, nowj, avgj, minj, maxj, 'COMMENT: \\n',	dtypek, nowk, avgk, mink, maxk, 'COMMENT: \\n',	dtypel, nowl, avgl, minl, maxl, 'COMMENT: \\n')
	else:
		rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start,
					'-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, DEFe, DEFf, DEFg, DEFh, DEFi, DEFj, DEFk, DEFl, 'COMMENT: \\n', 
					dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n', dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
					dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n', dtypee, nowe, avge, mine, maxe, 'COMMENT: \\n',	dtypef, nowf, avgf, minf, maxf, 'COMMENT: \\n',	
					dtypeg, nowg, avgg, ming, maxg, 'COMMENT: \\n',	dtypeh, nowh, avgh, minh, maxh, 'COMMENT: \\n',	dtypei, nowi, avgi, mini, maxi, 'COMMENT: \\n',	
					dtypej, nowj, avgj, minj, maxj, 'COMMENT: \\n',	dtypek, nowk, avgk, mink, maxk, 'COMMENT: \\n',	dtypel, nowl, avgl, minl, maxl, 'COMMENT: \\n')
###########3#################################################################################
def dItem16(data):
	pngname = str(data['pname'])
	start = data['stime']
	graphname = str(data['gname'] + " (" + data['graphid'] + ") " + data['host'] + "(" + data['flag'] + ")")
	DEFa = str(r"DEF:a="+data['rrdpath']+r':'+data['pitem'][0][0]+r":AVERAGE")
	DEFb = str(r"DEF:b="+data['rrdpath']+r':'+data['pitem'][1][0]+r":AVERAGE")
	DEFc = str(r"DEF:c="+data['rrdpath']+r':'+data['pitem'][2][0]+r":AVERAGE")
	DEFd = str(r"DEF:d="+data['rrdpath']+r':'+data['pitem'][3][0]+r":AVERAGE")
	DEFe = str(r"DEF:e="+data['rrdpath']+r':'+data['pitem'][4][0]+r":AVERAGE")
	DEFf = str(r"DEF:f="+data['rrdpath']+r':'+data['pitem'][5][0]+r":AVERAGE")
	DEFg = str(r"DEF:g="+data['rrdpath']+r':'+data['pitem'][6][0]+r":AVERAGE")
	DEFh = str(r"DEF:h="+data['rrdpath']+r':'+data['pitem'][7][0]+r":AVERAGE")
	DEFi = str(r"DEF:i="+data['rrdpath']+r':'+data['pitem'][8][0]+r":AVERAGE")
	DEFj = str(r"DEF:j="+data['rrdpath']+r':'+data['pitem'][9][0]+r":AVERAGE")
	DEFk = str(r"DEF:k="+data['rrdpath']+r':'+data['pitem'][10][0]+r":AVERAGE")
	DEFl = str(r"DEF:l="+data['rrdpath']+r':'+data['pitem'][11][0]+r":AVERAGE")
	DEFm = str(r"DEF:m="+data['rrdpath']+r':'+data['pitem'][12][0]+r":AVERAGE")
	DEFn = str(r"DEF:n="+data['rrdpath']+r':'+data['pitem'][13][0]+r":AVERAGE")
	DEFo = str(r"DEF:o="+data['rrdpath']+r':'+data['pitem'][14][0]+r":AVERAGE")
	DEFp = str(r"DEF:p="+data['rrdpath']+r':'+data['pitem'][15][0]+r":AVERAGE")
	unit = str(data['pitem'][0][2])
	if not unit:
		unit = ' '
	if data['cols'] or data['itypes']:
		if not data['cols']:
			dtypea = str(data['itypes'][0][0]+r":a#FAFD9EFF:"+data['pitem'][0][1])
			dtypeb = str(data['itypes'][0][1]+r":b#000000FF:"+data['pitem'][1][1])
			dtypec = str(data['itypes'][0][2]+r":c#FFF200FF:"+data['pitem'][2][1])
			dtyped = str(data['itypes'][0][3]+r":d#FF9900FF:"+data['pitem'][3][1])
			dtypee = str(data['itypes'][0][4]+r":e#FF5700FF:"+data['pitem'][4][1])
			dtypef = str(data['itypes'][0][4]+r":f#FF0000FF:"+data['pitem'][5][1])
			dtypeg = str(data['itypes'][0][6]+r":g#DE0056FF:"+data['pitem'][6][1])
			dtypeh = str(data['itypes'][0][7]+r":h#A150AAFF:"+data['pitem'][7][1])
			dtypei = str(data['itypes'][0][8]+r":i#8D00BAFF:"+data['pitem'][8][1])
			dtypej = str(data['itypes'][0][9]+r":j#6557D0FF:"+data['pitem'][9][1])
			dtypek = str(data['itypes'][0][10]+r":k#8D85F3FF:"+data['pitem'][10][1])
			dtypel = str(data['itypes'][0][11]+r":l#2175D9FF:"+data['pitem'][11][1])
			dtypem = str(data['itypes'][0][12]+r":m#0000FFFF:"+data['pitem'][12][1])
			dtypen = str(data['itypes'][0][13]+r":n#00A0C1FF:"+data['pitem'][13][1])
			dtypeo = str(data['itypes'][0][14]+r":o#96E78AFF:"+data['pitem'][14][1])
			dtypep = str(data['itypes'][0][15]+r":p#00CF00FF:"+data['pitem'][15][1])
		elif not data['itypes']:
			dtypea = str(r"LINE1:a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
			dtypeb = str(r"LINE1:b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
			dtypec = str(r"LINE1:c"+data['cols'][0][2]+r":"+data['pitem'][2][1])
			dtyped = str(r"LINE1:d"+data['cols'][0][3]+r":"+data['pitem'][3][1])
			dtypee = str(r"LINE1:e"+data['cols'][0][4]+r":"+data['pitem'][4][1])
			dtypef = str(r"LINE1:f"+data['cols'][0][5]+r":"+data['pitem'][5][1])
			dtypeg = str(r"LINE1:g"+data['cols'][0][6]+r":"+data['pitem'][6][1])
			dtypeh = str(r"LINE1:h"+data['cols'][0][7]+r":"+data['pitem'][7][1])
			dtypei = str(r"LINE1:i"+data['cols'][0][8]+r":"+data['pitem'][8][1])
			dtypej = str(r"LINE1:j"+data['cols'][0][9]+r":"+data['pitem'][9][1])
			dtypek = str(r"LINE1:k"+data['cols'][0][10]+r":"+data['pitem'][10][1])
			dtypel = str(r"LINE1:l"+data['cols'][0][11]+r":"+data['pitem'][11][1])
			dtypem = str(r"LINE1:m"+data['cols'][0][12]+r":"+data['pitem'][12][1])
			dtypen = str(r"LINE1:n"+data['cols'][0][13]+r":"+data['pitem'][13][1])
			dtypeo = str(r"LINE1:o"+data['cols'][0][14]+r":"+data['pitem'][14][1])
			dtypep = str(r"LINE1:p"+data['cols'][0][15]+r":"+data['pitem'][15][1])
		else:
			dtypea = str(data['itypes'][0][0]+r":a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
			dtypeb = str(data['itypes'][0][1]+r":b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
			dtypec = str(data['itypes'][0][2]+r":c"+data['cols'][0][2]+r":"+data['pitem'][2][1])
			dtyped = str(data['itypes'][0][3]+r":d"+data['cols'][0][3]+r":"+data['pitem'][3][1])
			dtypee = str(data['itypes'][0][4]+r":e"+data['cols'][0][4]+r":"+data['pitem'][4][1])
			dtypef = str(data['itypes'][0][5]+r":f"+data['cols'][0][5]+r":"+data['pitem'][5][1])
			dtypeg = str(data['itypes'][0][6]+r":g"+data['cols'][0][6]+r":"+data['pitem'][6][1])
			dtypeh = str(data['itypes'][0][7]+r":h"+data['cols'][0][7]+r":"+data['pitem'][7][1])
			dtypei = str(data['itypes'][0][8]+r":i"+data['cols'][0][8]+r":"+data['pitem'][8][1])
			dtypej = str(data['itypes'][0][9]+r":j"+data['cols'][0][9]+r":"+data['pitem'][9][1])
			dtypek = str(data['itypes'][0][10]+r":k"+data['cols'][0][10]+r":"+data['pitem'][10][1])
			dtypel = str(data['itypes'][0][11]+r":l"+data['cols'][0][11]+r":"+data['pitem'][11][1])
			dtypem = str(data['itypes'][0][12]+r":m"+data['cols'][0][12]+r":"+data['pitem'][12][1])
			dtypen = str(data['itypes'][0][13]+r":n"+data['cols'][0][13]+r":"+data['pitem'][13][1])
			dtypeo = str(data['itypes'][0][14]+r":o"+data['cols'][0][14]+r":"+data['pitem'][14][1])
			dtypep = str(data['itypes'][0][15]+r":p"+data['cols'][0][15]+r":"+data['pitem'][15][1])
	else:
		dtypea = str(r"LINE1:a#FAFD9EFF:"+data['pitem'][0][1])
		dtypeb = str(r"LINE1:b#000000FF:"+data['pitem'][1][1])
		dtypec = str(r"LINE1:c#FFF200FF:"+data['pitem'][2][1])
		dtyped = str(r"LINE1:d#FF9900FF:"+data['pitem'][3][1])
		dtypee = str(r"LINE1:e#FF5700FF:"+data['pitem'][4][1])
		dtypef = str(r"LINE1:f#FF0000FF:"+data['pitem'][5][1])
		dtypeg = str(r"LINE1:g#DE0056FF:"+data['pitem'][6][1])
		dtypeh = str(r"LINE1:h#A150AAFF:"+data['pitem'][7][1])
		dtypei = str(r"LINE1:i#8D00BAFF:"+data['pitem'][8][1])
		dtypej = str(r"LINE1:j#6557D0FF:"+data['pitem'][9][1])
		dtypek = str(r"LINE1:k#8D85F3FF:"+data['pitem'][10][1])
		dtypel = str(r"LINE1:l#2175D9FF:"+data['pitem'][11][1])
		dtypem = str(r"LINE1:m#0000FFFF:"+data['pitem'][12][1])
		dtypen = str(r"LINE1:n#00A0C1FF:"+data['pitem'][13][1])
		dtypeo = str(r"LINE1:o#96E78AFF:"+data['pitem'][14][1])
		dtypep = str(r"LINE1:p#00CF00FF:"+data['pitem'][15][1])
	maxa = 'GPRINT:a:MAX:Max\:%.2lf %s'
	mina = 'GPRINT:a:MIN:Min\:%.2lf %s'
	avga = 'GPRINT:a:AVERAGE:Avg\:%.2lf %s'
	nowa = 'GPRINT:a:LAST:Now\:%.2lf %s'
	maxb = 'GPRINT:b:MAX:Max\:%.2lf %s'
	minb = 'GPRINT:b:MIN:Min\:%.2lf %s'
	avgb = 'GPRINT:b:AVERAGE:Avg\:%.2lf %s'
	nowb = 'GPRINT:b:LAST:Now\:%.2lf %s'
	maxc = 'GPRINT:c:MAX:Max\:%.2lf %s'
	minc = 'GPRINT:c:MIN:Min\:%.2lf %s'
	avgc = 'GPRINT:c:AVERAGE:Avg\:%.2lf %s'
	nowc = 'GPRINT:c:LAST:Now\:%.2lf %s'
	maxd = 'GPRINT:d:MAX:Max\:%.2lf %s'
	mind = 'GPRINT:d:MIN:Min\:%.2lf %s'
	avgd = 'GPRINT:d:AVERAGE:Avg\:%.2lf %s'
	nowd = 'GPRINT:d:LAST:Now\:%.2lf %s'
	maxe = 'GPRINT:e:MAX:Max\:%.2lf %s'
	mine = 'GPRINT:e:MIN:Min\:%.2lf %s'
	avge = 'GPRINT:e:AVERAGE:Avg\:%.2lf %s'
	nowe = 'GPRINT:e:LAST:Now\:%.2lf %s'
	maxf = 'GPRINT:f:MAX:Max\:%.2lf %s'
	minf = 'GPRINT:f:MIN:Min\:%.2lf %s'
	avgf = 'GPRINT:f:AVERAGE:Avg\:%.2lf %s'
	nowf = 'GPRINT:f:LAST:Now\:%.2lf %s'
	maxg = 'GPRINT:g:MAX:Max\:%.2lf %s'
	ming = 'GPRINT:g:MIN:Min\:%.2lf %s'
	avgg = 'GPRINT:g:AVERAGE:Avg\:%.2lf %s'
	nowg = 'GPRINT:g:LAST:Now\:%.2lf %s'
	maxh = 'GPRINT:h:MAX:Max\:%.2lf %s'
	minh = 'GPRINT:h:MIN:Min\:%.2lf %s'
	avgh = 'GPRINT:h:AVERAGE:Avg\:%.2lf %s'
	nowh = 'GPRINT:h:LAST:Now\:%.2lf %s'
	maxi = 'GPRINT:i:MAX:Max\:%.2lf %s'
	mini = 'GPRINT:i:MIN:Min\:%.2lf %s'
	avgi = 'GPRINT:i:AVERAGE:Avg\:%.2lf %s'
	nowi = 'GPRINT:i:LAST:Now\:%.2lf %s'
	maxj = 'GPRINT:j:MAX:Max\:%.2lf %s'
	minj = 'GPRINT:j:MIN:Min\:%.2lf %s'
	avgj = 'GPRINT:j:AVERAGE:Avg\:%.2lf %s'
	nowj = 'GPRINT:j:LAST:Now\:%.2lf %s'
	maxk = 'GPRINT:k:MAX:Max\:%.2lf %s'
	mink = 'GPRINT:k:MIN:Min\:%.2lf %s'
	avgk = 'GPRINT:k:AVERAGE:Avg\:%.2lf %s'
	nowk = 'GPRINT:k:LAST:Now\:%.2lf %s'
	maxl = 'GPRINT:l:MAX:Max\:%.2lf %s'
	minl = 'GPRINT:l:MIN:Min\:%.2lf %s'
	avgl = 'GPRINT:l:AVERAGE:Avg\:%.2lf %s'
	nowl = 'GPRINT:l:LAST:Now\:%.2lf %s'
	maxm = 'GPRINT:m:MAX:Max\:%.2lf %s'
	minm = 'GPRINT:m:MIN:Min\:%.2lf %s'
	avgm = 'GPRINT:m:AVERAGE:Avg\:%.2lf %s'
	nowm = 'GPRINT:m:LAST:Now\:%.2lf %s'
	maxn = 'GPRINT:n:MAX:Max\:%.2lf %s'
	minn = 'GPRINT:n:MIN:Min\:%.2lf %s'
	avgn = 'GPRINT:n:AVERAGE:Avg\:%.2lf %s'
	nown = 'GPRINT:n:LAST:Now\:%.2lf %s'
	maxo = 'GPRINT:o:MAX:Max\:%.2lf %s'
	mino = 'GPRINT:o:MIN:Min\:%.2lf %s'
	avgo = 'GPRINT:o:AVERAGE:Avg\:%.2lf %s'
	nowo = 'GPRINT:o:LAST:Now\:%.2lf %s'
	maxp = 'GPRINT:p:MAX:Max\:%.2lf %s'
	minp = 'GPRINT:p:MIN:Min\:%.2lf %s'
	avgp = 'GPRINT:p:AVERAGE:Avg\:%.2lf %s'
	nowp = 'GPRINT:p:LAST:Now\:%.2lf %s'
	if data['flag'] == 'Daily':
		rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start, '-x', 'MINUTE:30:HOUR:2:HOUR:2:0:%H:%M',
					'-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, DEFe, DEFf, DEFg, DEFh, DEFi, DEFj, DEFk, DEFl, DEFm, DEFn, DEFo, DEFp, 'COMMENT: \\n', 
					dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n', dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
					dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n', dtypee, nowe, avge, mine, maxe, 'COMMENT: \\n',	dtypef, nowf, avgf, minf, maxf, 'COMMENT: \\n',	
					dtypeg, nowg, avgg, ming, maxg, 'COMMENT: \\n',	dtypeh, nowh, avgh, minh, maxh, 'COMMENT: \\n',	dtypei, nowi, avgi, mini, maxi, 'COMMENT: \\n',	
					dtypej, nowj, avgj, minj, maxj, 'COMMENT: \\n',	dtypek, nowk, avgk, mink, maxk, 'COMMENT: \\n',	dtypel, nowl, avgl, minl, maxl, 'COMMENT: \\n',
					dtypem, nowm, avgm, minm, maxm, 'COMMENT: \\n',	dtypen, nown, avgn, minn, maxn, 'COMMENT: \\n',	dtypeo, nowo, avgo, mino, maxo, 'COMMENT: \\n',
					dtypep, nowp, avgp, minp, maxp, 'COMMENT: \\n')
	elif data['flag'] == 'Weekly':
		rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start, '-x', 'HOUR:4:HOUR:12:DAY:1:0:%d',
					'-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, DEFe, DEFf, DEFg, DEFh, DEFi, DEFj, DEFk, DEFl, DEFm, DEFn, DEFo, DEFp, 'COMMENT: \\n', 
					dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n', dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
					dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n', dtypee, nowe, avge, mine, maxe, 'COMMENT: \\n',	dtypef, nowf, avgf, minf, maxf, 'COMMENT: \\n',	
					dtypeg, nowg, avgg, ming, maxg, 'COMMENT: \\n',	dtypeh, nowh, avgh, minh, maxh, 'COMMENT: \\n',	dtypei, nowi, avgi, mini, maxi, 'COMMENT: \\n',	
					dtypej, nowj, avgj, minj, maxj, 'COMMENT: \\n',	dtypek, nowk, avgk, mink, maxk, 'COMMENT: \\n',	dtypel, nowl, avgl, minl, maxl, 'COMMENT: \\n',
					dtypem, nowm, avgm, minm, maxm, 'COMMENT: \\n',	dtypen, nown, avgn, minn, maxn, 'COMMENT: \\n',	dtypeo, nowo, avgo, mino, maxo, 'COMMENT: \\n',
					dtypep, nowp, avgp, minp, maxp, 'COMMENT: \\n')
	else:
		rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start,
					'-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, DEFe, DEFf, DEFg, DEFh, DEFi, DEFj, DEFk, DEFl, DEFm, DEFn, DEFo, DEFp, 'COMMENT: \\n', 
					dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n', dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
					dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n', dtypee, nowe, avge, mine, maxe, 'COMMENT: \\n',	dtypef, nowf, avgf, minf, maxf, 'COMMENT: \\n',	
					dtypeg, nowg, avgg, ming, maxg, 'COMMENT: \\n',	dtypeh, nowh, avgh, minh, maxh, 'COMMENT: \\n',	dtypei, nowi, avgi, mini, maxi, 'COMMENT: \\n',	
					dtypej, nowj, avgj, minj, maxj, 'COMMENT: \\n',	dtypek, nowk, avgk, mink, maxk, 'COMMENT: \\n',	dtypel, nowl, avgl, minl, maxl, 'COMMENT: \\n',
					dtypem, nowm, avgm, minm, maxm, 'COMMENT: \\n',	dtypen, nown, avgn, minn, maxn, 'COMMENT: \\n',	dtypeo, nowo, avgo, mino, maxo, 'COMMENT: \\n',
					dtypep, nowp, avgp, minp, maxp, 'COMMENT: \\n')
###################################################################################3
def dItem24(data):
	pngname = str(data['pname'])
	start = data['stime']
	graphname = str(data['gname'] + " (" + data['graphid'] + ") " + data['host'] + "(" + data['flag'] + ")")
	DEFa = str(r"DEF:a="+data['rrdpath']+r':'+data['pitem'][0][0]+r":AVERAGE")
	DEFb = str(r"DEF:b="+data['rrdpath']+r':'+data['pitem'][1][0]+r":AVERAGE")
	DEFc = str(r"DEF:c="+data['rrdpath']+r':'+data['pitem'][2][0]+r":AVERAGE")
	DEFd = str(r"DEF:d="+data['rrdpath']+r':'+data['pitem'][3][0]+r":AVERAGE")
	DEFe = str(r"DEF:e="+data['rrdpath']+r':'+data['pitem'][4][0]+r":AVERAGE")
	DEFf = str(r"DEF:f="+data['rrdpath']+r':'+data['pitem'][5][0]+r":AVERAGE")
	DEFg = str(r"DEF:g="+data['rrdpath']+r':'+data['pitem'][6][0]+r":AVERAGE")
	DEFh = str(r"DEF:h="+data['rrdpath']+r':'+data['pitem'][7][0]+r":AVERAGE")
	DEFi = str(r"DEF:i="+data['rrdpath']+r':'+data['pitem'][8][0]+r":AVERAGE")
	DEFj = str(r"DEF:j="+data['rrdpath']+r':'+data['pitem'][9][0]+r":AVERAGE")
	DEFk = str(r"DEF:k="+data['rrdpath']+r':'+data['pitem'][10][0]+r":AVERAGE")
	DEFl = str(r"DEF:l="+data['rrdpath']+r':'+data['pitem'][11][0]+r":AVERAGE")
	DEFm = str(r"DEF:m="+data['rrdpath']+r':'+data['pitem'][12][0]+r":AVERAGE")
	DEFn = str(r"DEF:n="+data['rrdpath']+r':'+data['pitem'][13][0]+r":AVERAGE")
	DEFo = str(r"DEF:o="+data['rrdpath']+r':'+data['pitem'][14][0]+r":AVERAGE")
	DEFp = str(r"DEF:p="+data['rrdpath']+r':'+data['pitem'][15][0]+r":AVERAGE")
	DEFq = str(r"DEF:q="+data['rrdpath']+r':'+data['pitem'][16][0]+r":AVERAGE")
	DEFr = str(r"DEF:r="+data['rrdpath']+r':'+data['pitem'][17][0]+r":AVERAGE")
	DEFs = str(r"DEF:s="+data['rrdpath']+r':'+data['pitem'][18][0]+r":AVERAGE")
	DEFt = str(r"DEF:t="+data['rrdpath']+r':'+data['pitem'][19][0]+r":AVERAGE")
	DEFu = str(r"DEF:u="+data['rrdpath']+r':'+data['pitem'][20][0]+r":AVERAGE")
	DEFv = str(r"DEF:v="+data['rrdpath']+r':'+data['pitem'][21][0]+r":AVERAGE")
	DEFw = str(r"DEF:w="+data['rrdpath']+r':'+data['pitem'][22][0]+r":AVERAGE")
	DEFx = str(r"DEF:x="+data['rrdpath']+r':'+data['pitem'][23][0]+r":AVERAGE")
	unit = str(data['pitem'][0][2])
	if not unit:
		unit = ' '
	if data['cols'] or data['itypes']:
		if not data['cols']:
			dtypea = str(data['itypes'][0][0]+r":a#FFF200FF:"+data['pitem'][0][1])
			dtypeb = str(data['itypes'][0][1]+r":b#FF9900FF:"+data['pitem'][1][1])
			dtypec = str(data['itypes'][0][2]+r":c#FF5700FF:"+data['pitem'][2][1])
			dtyped = str(data['itypes'][0][3]+r":d#FF0000FF:"+data['pitem'][3][1])
			dtypee = str(data['itypes'][0][4]+r":e#DE0056FF:"+data['pitem'][4][1])
			dtypef = str(data['itypes'][0][4]+r":f#A150AAFF:"+data['pitem'][5][1])
			dtypeg = str(data['itypes'][0][6]+r":g#8D00BAFF:"+data['pitem'][6][1])
			dtypeh = str(data['itypes'][0][7]+r":h#6557D0FF:"+data['pitem'][7][1])
			dtypei = str(data['itypes'][0][8]+r":i#8D85F3FF:"+data['pitem'][8][1])
			dtypej = str(data['itypes'][0][9]+r":j#2175D9FF:"+data['pitem'][9][1])
			dtypek = str(data['itypes'][0][10]+r":k#0000FFFF:"+data['pitem'][10][1])
			dtypel = str(data['itypes'][0][11]+r":l#00A0C1FF:"+data['pitem'][11][1])
			dtypem = str(data['itypes'][0][12]+r":m#96E78AFF:"+data['pitem'][12][1])
			dtypen = str(data['itypes'][0][13]+r":n#00CF00FF:"+data['pitem'][13][1])
			dtypeo = str(data['itypes'][0][14]+r":o#157419FF:"+data['pitem'][14][1])
			dtypep = str(data['itypes'][0][15]+r":p#837C04FF:"+data['pitem'][15][1])
			dtypeq = str(data['itypes'][0][16]+r":q#FFC73BFF:"+data['pitem'][16][1])
			dtyper = str(data['itypes'][0][17]+r":r#FF00FFFF:"+data['pitem'][17][1])
			dtypes = str(data['itypes'][0][18]+r":s#ED7600FF:"+data['pitem'][18][1])
			dtypet = str(data['itypes'][0][19]+r":t#D8ACE0FF:"+data['pitem'][19][1])
			dtypeu = str(data['itypes'][0][20]+r":u#AFECEDFF:"+data['pitem'][20][1])
			dtypev = str(data['itypes'][0][21]+r":v#562B29FF:"+data['pitem'][21][1])
			dtypew = str(data['itypes'][0][22]+r":w#8F9286FF:"+data['pitem'][22][1])
			dtypex = str(data['itypes'][0][23]+r":x#837C04FF:"+data['pitem'][23][1])
		elif not data['itypes']:
			dtypea = str(r"LINE1:a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
			dtypeb = str(r"LINE1:b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
			dtypec = str(r"LINE1:c"+data['cols'][0][2]+r":"+data['pitem'][2][1])
			dtyped = str(r"LINE1:d"+data['cols'][0][3]+r":"+data['pitem'][3][1])
			dtypee = str(r"LINE1:e"+data['cols'][0][4]+r":"+data['pitem'][4][1])
			dtypef = str(r"LINE1:f"+data['cols'][0][5]+r":"+data['pitem'][5][1])
			dtypeg = str(r"LINE1:g"+data['cols'][0][6]+r":"+data['pitem'][6][1])
			dtypeh = str(r"LINE1:h"+data['cols'][0][7]+r":"+data['pitem'][7][1])
			dtypei = str(r"LINE1:i"+data['cols'][0][8]+r":"+data['pitem'][8][1])
			dtypej = str(r"LINE1:j"+data['cols'][0][9]+r":"+data['pitem'][9][1])
			dtypek = str(r"LINE1:k"+data['cols'][0][10]+r":"+data['pitem'][10][1])
			dtypel = str(r"LINE1:l"+data['cols'][0][11]+r":"+data['pitem'][11][1])
			dtypem = str(r"LINE1:m"+data['cols'][0][12]+r":"+data['pitem'][12][1])
			dtypen = str(r"LINE1:n"+data['cols'][0][13]+r":"+data['pitem'][13][1])
			dtypeo = str(r"LINE1:o"+data['cols'][0][14]+r":"+data['pitem'][14][1])
			dtypep = str(r"LINE1:p"+data['cols'][0][15]+r":"+data['pitem'][15][1])
			dtypeq = str(r"LINE1:q"+data['cols'][0][16]+r":"+data['pitem'][16][1])
			dtyper = str(r"LINE1:r"+data['cols'][0][17]+r":"+data['pitem'][17][1])
			dtypes = str(r"LINE1:s"+data['cols'][0][18]+r":"+data['pitem'][18][1])
			dtypet = str(r"LINE1:t"+data['cols'][0][19]+r":"+data['pitem'][19][1])
			dtypeu = str(r"LINE1:u"+data['cols'][0][20]+r":"+data['pitem'][20][1])
			dtypev = str(r"LINE1:v"+data['cols'][0][21]+r":"+data['pitem'][21][1])
			dtypew = str(r"LINE1:w"+data['cols'][0][22]+r":"+data['pitem'][22][1])
			dtypex = str(r"LINE1:x"+data['cols'][0][23]+r":"+data['pitem'][23][1])
		else:
			dtypea = str(data['itypes'][0][0]+r":a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
			dtypeb = str(data['itypes'][0][1]+r":b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
			dtypec = str(data['itypes'][0][2]+r":c"+data['cols'][0][2]+r":"+data['pitem'][2][1])
			dtyped = str(data['itypes'][0][3]+r":d"+data['cols'][0][3]+r":"+data['pitem'][3][1])
			dtypee = str(data['itypes'][0][4]+r":e"+data['cols'][0][4]+r":"+data['pitem'][4][1])
			dtypef = str(data['itypes'][0][5]+r":f"+data['cols'][0][5]+r":"+data['pitem'][5][1])
			dtypeg = str(data['itypes'][0][6]+r":g"+data['cols'][0][6]+r":"+data['pitem'][6][1])
			dtypeh = str(data['itypes'][0][7]+r":h"+data['cols'][0][7]+r":"+data['pitem'][7][1])
			dtypei = str(data['itypes'][0][8]+r":i"+data['cols'][0][8]+r":"+data['pitem'][8][1])
			dtypej = str(data['itypes'][0][9]+r":j"+data['cols'][0][9]+r":"+data['pitem'][9][1])
			dtypek = str(data['itypes'][0][10]+r":k"+data['cols'][0][10]+r":"+data['pitem'][10][1])
			dtypel = str(data['itypes'][0][11]+r":l"+data['cols'][0][11]+r":"+data['pitem'][11][1])
			dtypem = str(data['itypes'][0][12]+r":m"+data['cols'][0][12]+r":"+data['pitem'][12][1])
			dtypen = str(data['itypes'][0][13]+r":n"+data['cols'][0][13]+r":"+data['pitem'][13][1])
			dtypeo = str(data['itypes'][0][14]+r":o"+data['cols'][0][14]+r":"+data['pitem'][14][1])
			dtypep = str(data['itypes'][0][15]+r":p"+data['cols'][0][15]+r":"+data['pitem'][15][1])
			dtypeq = str(data['itypes'][0][16]+r":q"+data['cols'][0][16]+r":"+data['pitem'][16][1])
			dtyper = str(data['itypes'][0][17]+r":r"+data['cols'][0][17]+r":"+data['pitem'][17][1])
			dtypes = str(data['itypes'][0][18]+r":s"+data['cols'][0][18]+r":"+data['pitem'][18][1])
			dtypet = str(data['itypes'][0][19]+r":t"+data['cols'][0][19]+r":"+data['pitem'][19][1])
			dtypeu = str(data['itypes'][0][20]+r":u"+data['cols'][0][20]+r":"+data['pitem'][20][1])
			dtypev = str(data['itypes'][0][21]+r":v"+data['cols'][0][21]+r":"+data['pitem'][21][1])
			dtypew = str(data['itypes'][0][22]+r":w"+data['cols'][0][22]+r":"+data['pitem'][22][1])
			dtypex = str(data['itypes'][0][23]+r":x"+data['cols'][0][23]+r":"+data['pitem'][23][1])
	else:
		dtypea = str(r"LINE1:a#FFF200FF:"+data['pitem'][0][1])
		dtypeb = str(r"LINE1:b#FF9900FF:"+data['pitem'][1][1])
		dtypec = str(r"LINE1:c#FF5700FF:"+data['pitem'][2][1])
		dtyped = str(r"LINE1:d#FF0000FF:"+data['pitem'][3][1])
		dtypee = str(r"LINE1:e#DE0056FF:"+data['pitem'][4][1])
		dtypef = str(r"LINE1:f#A150AAFF:"+data['pitem'][5][1])
		dtypeg = str(r"LINE1:g#8D00BAFF:"+data['pitem'][6][1])
		dtypeh = str(r"LINE1:h#6557D0FF:"+data['pitem'][7][1])
		dtypei = str(r"LINE1:i#8D85F3FF:"+data['pitem'][8][1])
		dtypej = str(r"LINE1:j#2175D9FF:"+data['pitem'][9][1])
		dtypek = str(r"LINE1:k#0000FFFF:"+data['pitem'][10][1])
		dtypel = str(r"LINE1:l#00A0C1FF:"+data['pitem'][11][1])
		dtypem = str(r"LINE1:m#96E78AFF:"+data['pitem'][12][1])
		dtypen = str(r"LINE1:n#00CF00FF:"+data['pitem'][13][1])
		dtypeo = str(r"LINE1:o#157419FF:"+data['pitem'][14][1])
		dtypep = str(r"LINE1:p#837C04FF:"+data['pitem'][15][1])
		dtypeq = str(r"LINE1:q#FFC73BFF:"+data['pitem'][16][1])
		dtyper = str(r"LINE1:r#FF00FFFF:"+data['pitem'][17][1])
		dtypes = str(r"LINE1:s#ED7600FF:"+data['pitem'][18][1])
		dtypet = str(r"LINE1:t#D8ACE0FF:"+data['pitem'][19][1])
		dtypeu = str(r"LINE1:u#AFECEDFF:"+data['pitem'][20][1])
		dtypev = str(r"LINE1:v#562B29FF:"+data['pitem'][21][1])
		dtypew = str(r"LINE1:w#8F9286FF:"+data['pitem'][22][1])
		dtypex = str(r"LINE1:x#837C04FF:"+data['pitem'][23][1])
	maxa = 'GPRINT:a:MAX:Max\:%.2lf %s'
	mina = 'GPRINT:a:MIN:Min\:%.2lf %s'
	avga = 'GPRINT:a:AVERAGE:Avg\:%.2lf %s'
	nowa = 'GPRINT:a:LAST:Now\:%.2lf %s'
	maxb = 'GPRINT:b:MAX:Max\:%.2lf %s'
	minb = 'GPRINT:b:MIN:Min\:%.2lf %s'
	avgb = 'GPRINT:b:AVERAGE:Avg\:%.2lf %s'
	nowb = 'GPRINT:b:LAST:Now\:%.2lf %s'
	maxc = 'GPRINT:c:MAX:Max\:%.2lf %s'
	minc = 'GPRINT:c:MIN:Min\:%.2lf %s'
	avgc = 'GPRINT:c:AVERAGE:Avg\:%.2lf %s'
	nowc = 'GPRINT:c:LAST:Now\:%.2lf %s'
	maxd = 'GPRINT:d:MAX:Max\:%.2lf %s'
	mind = 'GPRINT:d:MIN:Min\:%.2lf %s'
	avgd = 'GPRINT:d:AVERAGE:Avg\:%.2lf %s'
	nowd = 'GPRINT:d:LAST:Now\:%.2lf %s'
	maxe = 'GPRINT:e:MAX:Max\:%.2lf %s'
	mine = 'GPRINT:e:MIN:Min\:%.2lf %s'
	avge = 'GPRINT:e:AVERAGE:Avg\:%.2lf %s'
	nowe = 'GPRINT:e:LAST:Now\:%.2lf %s'
	maxf = 'GPRINT:f:MAX:Max\:%.2lf %s'
	minf = 'GPRINT:f:MIN:Min\:%.2lf %s'
	avgf = 'GPRINT:f:AVERAGE:Avg\:%.2lf %s'
	nowf = 'GPRINT:f:LAST:Now\:%.2lf %s'
	maxg = 'GPRINT:g:MAX:Max\:%.2lf %s'
	ming = 'GPRINT:g:MIN:Min\:%.2lf %s'
	avgg = 'GPRINT:g:AVERAGE:Avg\:%.2lf %s'
	nowg = 'GPRINT:g:LAST:Now\:%.2lf %s'
	maxh = 'GPRINT:h:MAX:Max\:%.2lf %s'
	minh = 'GPRINT:h:MIN:Min\:%.2lf %s'
	avgh = 'GPRINT:h:AVERAGE:Avg\:%.2lf %s'
	nowh = 'GPRINT:h:LAST:Now\:%.2lf %s'
	maxi = 'GPRINT:i:MAX:Max\:%.2lf %s'
	mini = 'GPRINT:i:MIN:Min\:%.2lf %s'
	avgi = 'GPRINT:i:AVERAGE:Avg\:%.2lf %s'
	nowi = 'GPRINT:i:LAST:Now\:%.2lf %s'
	maxj = 'GPRINT:j:MAX:Max\:%.2lf %s'
	minj = 'GPRINT:j:MIN:Min\:%.2lf %s'
	avgj = 'GPRINT:j:AVERAGE:Avg\:%.2lf %s'
	nowj = 'GPRINT:j:LAST:Now\:%.2lf %s'
	maxk = 'GPRINT:k:MAX:Max\:%.2lf %s'
	mink = 'GPRINT:k:MIN:Min\:%.2lf %s'
	avgk = 'GPRINT:k:AVERAGE:Avg\:%.2lf %s'
	nowk = 'GPRINT:k:LAST:Now\:%.2lf %s'
	maxl = 'GPRINT:l:MAX:Max\:%.2lf %s'
	minl = 'GPRINT:l:MIN:Min\:%.2lf %s'
	avgl = 'GPRINT:l:AVERAGE:Avg\:%.2lf %s'
	nowl = 'GPRINT:l:LAST:Now\:%.2lf %s'
	maxm = 'GPRINT:m:MAX:Max\:%.2lf %s'
	minm = 'GPRINT:m:MIN:Min\:%.2lf %s'
	avgm = 'GPRINT:m:AVERAGE:Avg\:%.2lf %s'
	nowm = 'GPRINT:m:LAST:Now\:%.2lf %s'
	maxn = 'GPRINT:n:MAX:Max\:%.2lf %s'
	minn = 'GPRINT:n:MIN:Min\:%.2lf %s'
	avgn = 'GPRINT:n:AVERAGE:Avg\:%.2lf %s'
	nown = 'GPRINT:n:LAST:Now\:%.2lf %s'
	maxo = 'GPRINT:o:MAX:Max\:%.2lf %s'
	mino = 'GPRINT:o:MIN:Min\:%.2lf %s'
	avgo = 'GPRINT:o:AVERAGE:Avg\:%.2lf %s'
	nowo = 'GPRINT:o:LAST:Now\:%.2lf %s'
	maxp = 'GPRINT:p:MAX:Max\:%.2lf %s'
	minp = 'GPRINT:p:MIN:Min\:%.2lf %s'
	avgp = 'GPRINT:p:AVERAGE:Avg\:%.2lf %s'
	nowp = 'GPRINT:p:LAST:Now\:%.2lf %s'
	maxq = 'GPRINT:q:MAX:Max\:%.2lf %s'
	minq = 'GPRINT:q:MIN:Min\:%.2lf %s'
	avgq = 'GPRINT:q:AVERAGE:Avg\:%.2lf %s'
	nowq = 'GPRINT:q:LAST:Now\:%.2lf %s'
	maxr = 'GPRINT:r:MAX:Max\:%.2lf %s'
	minr = 'GPRINT:r:MIN:Min\:%.2lf %s'
	avgr = 'GPRINT:r:AVERAGE:Avg\:%.2lf %s'
	nowr = 'GPRINT:r:LAST:Now\:%.2lf %s'
	maxs = 'GPRINT:s:MAX:Max\:%.2lf %s'
	mins = 'GPRINT:s:MIN:Min\:%.2lf %s'
	avgs = 'GPRINT:s:AVERAGE:Avg\:%.2lf %s'
	nows = 'GPRINT:s:LAST:Now\:%.2lf %s'
	maxt = 'GPRINT:t:MAX:Max\:%.2lf %s'
	mint = 'GPRINT:t:MIN:Min\:%.2lf %s'
	avgt = 'GPRINT:t:AVERAGE:Avg\:%.2lf %s'
	nowt = 'GPRINT:t:LAST:Now\:%.2lf %s'
	maxu = 'GPRINT:u:MAX:Max\:%.2lf %s'
	minu = 'GPRINT:u:MIN:Min\:%.2lf %s'
	avgu = 'GPRINT:u:AVERAGE:Avg\:%.2lf %s'
	nowu = 'GPRINT:u:LAST:Now\:%.2lf %s'
	maxv = 'GPRINT:v:MAX:Max\:%.2lf %s'
	minv = 'GPRINT:v:MIN:Min\:%.2lf %s'
	avgv = 'GPRINT:v:AVERAGE:Avg\:%.2lf %s'
	nowv = 'GPRINT:v:LAST:Now\:%.2lf %s'
	maxw = 'GPRINT:w:MAX:Max\:%.2lf %s'
	minw = 'GPRINT:w:MIN:Min\:%.2lf %s'
	avgw = 'GPRINT:w:AVERAGE:Avg\:%.2lf %s'
	noww = 'GPRINT:w:LAST:Now\:%.2lf %s'
	maxx = 'GPRINT:x:MAX:Max\:%.2lf %s'
	minx = 'GPRINT:x:MIN:Min\:%.2lf %s'
	avgx = 'GPRINT:x:AVERAGE:Avg\:%.2lf %s'
	nowx = 'GPRINT:x:LAST:Now\:%.2lf %s'
	if data['flag'] == 'Daily':
		rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start, '-x', 'MINUTE:30:HOUR:2:HOUR:2:0:%H:%M',
					'-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, DEFe, DEFf, DEFg, DEFh, DEFi, DEFj, DEFk, DEFl, DEFm, DEFn, DEFo, DEFp, 
					DEFq, DEFr, DEFs, DEFt, DEFu, DEFv, DEFw, DEFx, 'COMMENT: \\n', 
					dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n', dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
					dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n', dtypee, nowe, avge, mine, maxe, 'COMMENT: \\n',	dtypef, nowf, avgf, minf, maxf, 'COMMENT: \\n',	
					dtypeg, nowg, avgg, ming, maxg, 'COMMENT: \\n',	dtypeh, nowh, avgh, minh, maxh, 'COMMENT: \\n',	dtypei, nowi, avgi, mini, maxi, 'COMMENT: \\n',	
					dtypej, nowj, avgj, minj, maxj, 'COMMENT: \\n',	dtypek, nowk, avgk, mink, maxk, 'COMMENT: \\n',	dtypel, nowl, avgl, minl, maxl, 'COMMENT: \\n',
					dtypem, nowm, avgm, minm, maxm, 'COMMENT: \\n',	dtypen, nown, avgn, minn, maxn, 'COMMENT: \\n',	dtypeo, nowo, avgo, mino, maxo, 'COMMENT: \\n',
					dtypep, nowp, avgp, minp, maxp, 'COMMENT: \\n', dtypeq, nowq, avgq, minq, maxq, 'COMMENT: \\n',	dtyper, nowr, avgr, minr, maxr, 'COMMENT: \\n',	
					dtypes, nows, avgs, mins, maxs, 'COMMENT: \\n',	dtypet, nowt, avgt, mint, maxt, 'COMMENT: \\n',	dtypeu, nowu, avgu, minu, maxu, 'COMMENT: \\n',	
					dtypev, nowv, avgv, minv, maxv, 'COMMENT: \\n',	dtypew, noww, avgw, minw, maxw, 'COMMENT: \\n',	dtypex, nowx, avgx, minx, maxx, 'COMMENT: \\n')
	elif data['flag'] == 'Weekly':
		rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start, '-x', 'HOUR:4:HOUR:12:DAY:1:0:%d',
					'-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, DEFe, DEFf, DEFg, DEFh, DEFi, DEFj, DEFk, DEFl, DEFm, DEFn, DEFo, DEFp, 
					DEFq, DEFr, DEFs, DEFt, DEFu, DEFv, DEFw, DEFx, 'COMMENT: \\n', 
					dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n', dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
					dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n', dtypee, nowe, avge, mine, maxe, 'COMMENT: \\n',	dtypef, nowf, avgf, minf, maxf, 'COMMENT: \\n',	
					dtypeg, nowg, avgg, ming, maxg, 'COMMENT: \\n',	dtypeh, nowh, avgh, minh, maxh, 'COMMENT: \\n',	dtypei, nowi, avgi, mini, maxi, 'COMMENT: \\n',	
					dtypej, nowj, avgj, minj, maxj, 'COMMENT: \\n',	dtypek, nowk, avgk, mink, maxk, 'COMMENT: \\n',	dtypel, nowl, avgl, minl, maxl, 'COMMENT: \\n',
					dtypem, nowm, avgm, minm, maxm, 'COMMENT: \\n',	dtypen, nown, avgn, minn, maxn, 'COMMENT: \\n',	dtypeo, nowo, avgo, mino, maxo, 'COMMENT: \\n',
					dtypep, nowp, avgp, minp, maxp, 'COMMENT: \\n', dtypeq, nowq, avgq, minq, maxq, 'COMMENT: \\n',	dtyper, nowr, avgr, minr, maxr, 'COMMENT: \\n',	
					dtypes, nows, avgs, mins, maxs, 'COMMENT: \\n',	dtypet, nowt, avgt, mint, maxt, 'COMMENT: \\n',	dtypeu, nowu, avgu, minu, maxu, 'COMMENT: \\n',	
					dtypev, nowv, avgv, minv, maxv, 'COMMENT: \\n',	dtypew, noww, avgw, minw, maxw, 'COMMENT: \\n',	dtypex, nowx, avgx, minx, maxx, 'COMMENT: \\n')
	else:
		rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start,
					'-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, DEFe, DEFf, DEFg, DEFh, DEFi, DEFj, DEFk, DEFl, DEFm, DEFn, DEFo, DEFp, 
					DEFq, DEFr, DEFs, DEFt, DEFu, DEFv, DEFw, DEFx, 'COMMENT: \\n', 
					dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n', dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n', dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
					dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n', dtypee, nowe, avge, mine, maxe, 'COMMENT: \\n',	dtypef, nowf, avgf, minf, maxf, 'COMMENT: \\n',	
					dtypeg, nowg, avgg, ming, maxg, 'COMMENT: \\n',	dtypeh, nowh, avgh, minh, maxh, 'COMMENT: \\n',	dtypei, nowi, avgi, mini, maxi, 'COMMENT: \\n',	
					dtypej, nowj, avgj, minj, maxj, 'COMMENT: \\n',	dtypek, nowk, avgk, mink, maxk, 'COMMENT: \\n',	dtypel, nowl, avgl, minl, maxl, 'COMMENT: \\n',
					dtypem, nowm, avgm, minm, maxm, 'COMMENT: \\n',	dtypen, nown, avgn, minn, maxn, 'COMMENT: \\n',	dtypeo, nowo, avgo, mino, maxo, 'COMMENT: \\n',
					dtypep, nowp, avgp, minp, maxp, 'COMMENT: \\n', dtypeq, nowq, avgq, minq, maxq, 'COMMENT: \\n',	dtyper, nowr, avgr, minr, maxr, 'COMMENT: \\n',	
					dtypes, nows, avgs, mins, maxs, 'COMMENT: \\n',	dtypet, nowt, avgt, mint, maxt, 'COMMENT: \\n',	dtypeu, nowu, avgu, minu, maxu, 'COMMENT: \\n',	
					dtypev, nowv, avgv, minv, maxv, 'COMMENT: \\n',	dtypew, noww, avgw, minw, maxw, 'COMMENT: \\n',	dtypex, nowx, avgx, minx, maxx, 'COMMENT: \\n')
################################################################
def drawmain(gdata):
	for data in gdata:
		nitem = len(data['pitem'])
		if nitem == 1:
			dItem01(data)
		elif nitem == 2:
			dItem02(data)
		elif nitem == 3:
			dItem03(data)
		elif nitem == 4:
			dItem04(data)
		elif nitem == 5:
			dItem05(data)
		elif nitem == 6:
			dItem06(data)
		elif nitem == 8:
			dItem08(data)
		elif nitem == 11:
			dItem11(data)
		elif nitem == 12:
			dItem12(data)
		elif nitem == 16:
			dItem16(data)
		elif nitem == 24:
			dItem24(data)
		#print data['pitem']
	
if __name__ == "__main__":
	drawmain()
