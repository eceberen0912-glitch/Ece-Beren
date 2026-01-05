"""Simple Bot class example.

Bu dosya eğitim amaçlı basit bir `Bot` sınıfı içerir: `start`, `stop`,
ve `handle_message` metodları bulunmaktadır.
"""

from typing import Dict



class Bot:
	"""Basit etkileşimli bot.

	Davranış:
	- Kullanıcının öğrenmek istediği konuyu sorar.
	- Eğer konu kirlilik sorunlarını aşmakla ilgiliyse proje önerileri sunar.
	- Eğer kullanıcı bir element/madde girerse, geri dönüştürülüp dönüştürülemeyeceğini ve türünü söyler.
	- Diğer konularda "bu konuda geliştirilmedim" diyerek yanıt verir.
	"""

	def __init__(self, name: str = "ÇevreBot") -> None:
		self.name = name
		self.running = False
		self.materials: Dict[str, Dict[str, str]] = self._build_material_db()
		self.pollution_keywords = [
			"kirlilik",
			"hava kirliliği",
			"su kirliliği",
			"atı",
			"atık",
			"çevre",
			"kirlilik sorunlarını",
		]

	def _build_material_db(self) -> Dict[str, Dict[str, str]]:
		return {
			"plastik": {"recyclable": "Evet (çeşide bağlı)", "type": "Plastik (PET, HDPE vb.)"},
			"pet": {"recyclable": "Evet", "type": "Plastik (PET)"},
			"cam": {"recyclable": "Evet", "type": "Cam"},
			"kağıt": {"recyclable": "Evet", "type": "Kağıt"},
			"karton": {"recyclable": "Evet", "type": "Karton / Kağıt"},
			"alüminyum": {"recyclable": "Evet", "type": "Metal (Alüminyum)"},
			"çelik": {"recyclable": "Evet", "type": "Metal (Çelik)"},
			"pil": {"recyclable": "Hayır (tehlikeli atık - özel toplama)", "type": "Pil / Kimyasal"},
			"elektronik": {"recyclable": "Evet (e-atık toplanmalı)", "type": "Elektronik / E-atık"},
			"organik": {"recyclable": "Hayır (kompostlanabilir)", "type": "Organik / Biyolojik"},
			"plastik poşet": {"recyclable": "Genelde hayır (özel işlemler)", "type": "Plastik"},
			"cam şişe": {"recyclable": "Evet", "type": "Cam"},
		}

	def start(self) -> None:
		self.running = True
		print(f"{self.name} başlatıldı.")

	def stop(self) -> None:
		self.running = False
		print(f"{self.name} durduruldu.")

	def _is_pollution_topic(self, text: str) -> bool:
		t = text.lower()
		return any(k in t for k in self.pollution_keywords)

	def _material_lookup(self, text: str) -> Dict[str, str]:
		t = text.lower().strip()
		# Tam eşleşme veya anahtar kelime içeriyorsa döndür
		for key in self.materials:
			if key == t or key in t:
				return self.materials[key]
		return {}

	def _pollution_project_suggestions(self) -> str:
		suggestions = [
			"Toplum temizlik ve bilinçlendirme kampanyası",
			"Atık ayırma ve geri dönüşüm istasyonu kurulumu",
			"Yağmur bahçeleri / yağmur suyu yönetimi projeleri",
			"Yerel hava kalitesi sensör ağı ve veri paylaşımı",
			"Geri dönüşümlü ürün tasarımı ve atık azaltma çalışmaları"
			"okul ve topluluklarda çevre eğitim programları"
            "ağaç dikme ve yeşil alan oluşturma etkinlikleri"]
		return "Öneri projeler:\n" + "\n".join(f"- {s}" for s in suggestions)

	def handle_message(self, message: str) -> str:
		m = message.strip()
		if not m:
			return "Lütfen bir şey yazın."

		# Öncelik: malzeme sorgusu
		mat = self._material_lookup(m)
		if mat:
			return f"Tür: {mat['type']}. Geri dönüştürülebilirlik: {mat['recyclable']}."

		# Kirlilik ile ilgili mi?
		if self._is_pollution_topic(m):
			return self._pollution_project_suggestions()

		# Diğer konular için yetkin değil
		return "Bu konuda geliştirilmedim. Başka bir şey sorabilir misin?"


def main() -> None:
	bot = Bot()
	bot.start()
	print("Merhaba! Bugün ne öğrenmek istiyorsun? (çıkış için 'çıkış' yaz)")
	while True:
		try:
			user = input("> ").strip()
		except (EOFError, KeyboardInterrupt):
			print()
			break

		if user.lower() in ("çıkış", "exit", "quit"):
			break

		response = bot.handle_message(user)
		print(response)

	bot.stop()


if __name__ == "__main__":
	main()
	bot.run("")
