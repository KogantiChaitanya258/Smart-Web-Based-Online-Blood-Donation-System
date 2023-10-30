import matplotlib.pyplot as plt
import base64
from io import BytesIO

def getgraph():
	buffer=BytesIO()
	plt.savefig(buffer, format='png') 
	buffer.seek(0)
	image_png=buffer.getvalue()
	graph = base64.b64encode(image_png)
	graph = graph.decode('utf-8')
	buffer.close()
	return graph

def getplot(x,y):
	plt.switch_backend('AGG')
	plt.figure(figsize=(5.5,4))
	plt.title('DONORS vs BLOODGROUPS')
	plt.bar(x,y, align='center', alpha=0.5,color='red')
	plt.xticks(rotation=45)
	plt.xlabel('Blood Groups')
	plt.ylabel('Donors Count')
	plt.tight_layout()


	graph=getgraph()
	return graph

def getplot1(x,y):
	plt.switch_backend('AGG')
	plt.figure(figsize=(5.5,4))
	plt.title('CITIES vs DONORS')
	plt.bar(x,y, align='center', alpha=0.5,color='red')
	plt.xticks(rotation=45)
	plt.ylabel('Donors Count')
	plt.xlabel('Cities')
	plt.tight_layout()


	graph=getgraph()
	return graph