import os
import time
import bmab

from bmab import utils
from bmab.nodes.binder import BMABBind
from bmab.external.advanced_clip import advanced_encode


question = '''
make detailed prompt for stable diffusion using keyword "{text}" about scene, lighting, face, pose, clothes, background and colors in only 1 sentence. The sentence is describes very detailed. Do not say about human race.
'''

class BMABGoogleGemini:

	def __init__(self) -> None:
		super().__init__()
		self.last_prompt = None
		self.last_seed = None

	@classmethod
	def INPUT_TYPES(s):
		return {
			'required': {
				'seed': ('INT', {'default': 0, 'min': 0, 'max': 0xffffffffffffffff}),
				'prompt': ('STRING', {'multiline': True, 'dynamicPrompts': True}),
				'text': ('STRING', {'multiline': True, 'dynamicPrompts': True}),
				'api_key': ('STRING', {'multiline': False}),
			}
		}

	RETURN_TYPES = ('STRING',)
	RETURN_NAMES = ('string', )
	FUNCTION = 'prompt'

	CATEGORY = 'BMAB/toy'

	def prompt(self, seed, prompt: str, text: str, api_key):
		if self.last_seed is None or (self.last_seed is not None and self.last_seed != seed):
			import google.generativeai as genai
			genai.configure(api_key=api_key)
			model = genai.GenerativeModel('gemini-pro')

			text = text.strip()
			response = model.generate_content(question.format(text=text))
			self.last_seed = seed
			self.last_prompt = response.text
			cache_path = os.path.join(os.path.dirname(bmab.__file__), '../resources/cache')
			cache_file = os.path.join(cache_path, 'gemini.txt')
			with open(cache_file, 'a', encoding='utf8') as f:
				f.write(time.strftime('%Y.%m.%d - %H:%M:%S'))
				f.write('\n')
				f.write(self.last_prompt)
				f.write('\n')
		if self.last_prompt is not None and prompt.find('__prompt__') >= 0:
			prompt = prompt.replace('__prompt__', self.last_prompt)
		return (prompt, )
