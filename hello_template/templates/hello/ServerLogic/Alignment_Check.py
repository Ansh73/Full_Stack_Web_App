import signal  
import sys  
import asyncio 
import aiohttp  
import json
import elementpath
import xml.etree.ElementTree as ET
from Bio.Blast import NCBIWWW
from itertools import islice
import concurrent.futures

class Alignment_Check:
	def __init__(self):
		#my dictionary
		self.genome_key_dict = {'nc_000852':'Paramecium bursaria Chlorella virus 1 [Organism]', 'nc_007346':'Emiliania huxleyi virus 86 [Organism]',
					'nc_008724':'Acanthocystis turfacea Chlorella virus 1 [Organism]', 'nc_009899':'Paramecium bursaria Chlorella virus AR158 [Organism]',
					'nc_014637':'Cafeteria roenbergensis virus BV-PW1 [Organism]', 'nc_020104':'Acanthamoeba polyphaga moumouvirus [Organism]',
					'nc_023423':'Pithovirus sibericum isolate P1084-T [Organism]', 'nc_016072' : 'Megavirus chiliensis [Organism]',
					'nc_023719':'Bacillus phage G [Organism]', 'nc_027867': 'Mollivirus sibericum isolate P1084-T [Organism]'}
		#self.loop = asyncio.get_event_loop()  
		#self.client = aiohttp.ClientSession(loop=loop)
	
	def blocking_io(self, genome_key, query_string):
		return NCBIWWW.qblast("blastn","nt",query_string,megablast=False,expect="1000",word_size="7",nucl_reward="1",nucl_penalty="-3",gapcosts="5 2",entrez_query=self.genome_key_dict[genome_key])
	
	async def get_xml(self, genome_key, query_string):  
		print("Anshul in get_xml")
		#res = await loop.run_in_executor(None, NCBIWWW.qblast("blastn","nt",query_string,megablast=False,expect="1000",word_size="7",nucl_reward="1",nucl_penalty="-3",gapcosts="5 2",entrez_query=self.genome_key_dict[genome_key]))
		#await res
		loop = asyncio.get_event_loop()
		with concurrent.futures.ThreadPoolExecutor() as pool:
			result = loop.run_in_executor(pool, self.blocking_io, genome_key,query_string)
			print('Anshul custom thread pool', result)
		#future1 = loop.run_in_executor(None, self.blocking_io, genome_key,query_string)
		#asyncio.sleep(0.0001)
		#return future1
		#print("Anshul trying to return response", res.result())
		#return response.read();

	async def get_max_alignment(self, genome_key, query_string,loop):  
		#data1 = await get_json(client, 'https://www.reddit.com/r/' + subreddit + '/top.json?sort=top&t=day&limit=5')
		result_handle = await loop.create_task(self.get_xml(genome_key, query_string)) 
		print("Anshul response received")
		response_xml_as_string = result_handle.result().read()
		responseXml = ET.fromstring(response_xml_as_string)
		a_from = [ (p.find('Hsp_hit-from').text, p.find('Hsp_hit-to').text) for p in islice(responseXml.iter('Hsp'), 0, 1)]
		print("Anshul returning", a_from)
		return (a_from)
		#print testId.text

	async def signal_handler(self, signal, frame):  
		loop.stop()
		client.close()
		sys.exit(0)
	signal.signal(signal.SIGINT, signal_handler)
	
	async def getMatchingLocations(self,query, loop):
		#import asyncio
		#tasks = []
		
		#myObj = Alignment_Check()
		print("Anshul the query is" + query)
		#asyncio.ensure_future(get_max_alignment('nc_000852', query, client))  
		#asyncio.ensure_future(get_max_alignment('nc_007346', query, client))  
		#asyncio.ensure_future(get_max_alignment('nc_008724', query, client))
		r1 = loop.create_task(asyncio.wait_for(self.get_max_alignment("nc_009899", query, loop), 5))
		await asyncio.wait([r1])
		return r1
		#task = asyncio.ensure_future(self.get_max_alignment("nc_009899", query))
		#asyncio.ensure_future(get_max_alignment('nc_014637', query, client))
		#asyncio.ensure_future(get_max_alignment('nc_016072', query, client))
		#asyncio.ensure_future(get_max_alignment('nc_016072', query, client))
		#asyncio.ensure_future(get_max_alignment('nc_020104', query, client))
		#asyncio.ensure_future(get_max_alignment('nc_023423', query, client))
		#asyncio.ensure_future(get_max_alignment('nc_023719', query, client))
		#asyncio.ensure_future(get_max_alignment('nc_027867', query, client))
		#loop.run_forever()