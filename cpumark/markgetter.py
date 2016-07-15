# -*- coding: utf-8 -*-
import urllib2

response_cpu = urllib2.urlopen(u'http://www.cpubenchmark.net/cpu_list.php')
cpupage = response_cpu.read()

f_cpu = open("output/source/cpupage.html","w")
f_cpu.write(cpupage)
f_cpu.close()


response_gpu = urllib2.urlopen(u'http://www.videocardbenchmark.net/gpu_list.php')
gpupage = response_gpu.read()

f_gpu = open("output/source/gpupage.html","w")
f_gpu.write(gpupage)
f_gpu.close()


response_gamemark = urllib2.urlopen(u'http://www.notebookcheck.net/Computer-Games-on-Laptop-Graphic-Cards.13849.0.html')
gamemarkpage = response_gamemark.read()

f_gpu = open("output/source/gamemark.html","w")
f_gpu.write(gamemarkpage)
f_gpu.close()