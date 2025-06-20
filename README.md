# 📖 Storymaker

Storymaker, yapay zeka desteğiyle çocuklara yönelik hikayeler oluşturan bir uygulamadır. İki farklı şekilde hikaye üretimi mümkündür:

1. **Serbest Mod:** Kullanıcının girdiği prompt, doğrudan bir LLM'e (Large Language Model) gönderilir ve modelden gelen yanıt hikaye olarak sunulur.
2. **RAG Tabanlı Mod:** Daha yenilikçi ve kontrollü olan bu yöntemde, önceden hazırlanmış veri kullanılarak Retrieval-Augmented Generation (RAG) yöntemiyle hikaye üretilir.

RAG modunda, hikayenin bileşenlerini oluşturan 8 farklı kategoriye ayrılmış örnekler vektör veritabanına (vector database) kaydedilir:
- `Main_character`
- `Environment`
- `Main_conflict`
- `Moral`
- `Plot`
- `Character_goal`
- `Genre`
- `Final_type`

Kullanıcının verdiği prompt, bu vektör veritabanında her kategori için semantik olarak en yakın 3 örneği bulmak için sorgulanır. Ardından her kategoriden rastgele bir örnek seçilir ve bu 8 bileşen, LLM'e input olarak gönderilir. Model bu yapıdan yola çıkarak bütünsel bir hikaye üretir.

Bu yöntemin avantajı:
- LLM'e yeniden eğitim gerekmeden yaratıcı ve kontrollü içerik üretilmesi,
- Çocuklara uygunluğu artırmak için çıktının daha kontrollü bir şekilde sınırlandırılması,
- Kullanıcının verdiği girdinin belirli bir ölçüde esnetilerek örnek tabana uygun hale getirilmesi.

---

## 🤖 Neden RAG Kullandım?

RAG, büyük dil modellerine daha anlamlı ve yönlendirilmiş veri sağlayarak:
- Üretkenliği artırır,
- Tutarlılığı korur,
- Kullanıcı girdilerini toleranslı şekilde yorumlayabilir.

Ayrıca model eğitimi gerektirmeden anlamlı çıktılar üretmeye olanak sağlar. Bu, özellikle çocuklar için içerik üretirken güvenlik ve kalite açısından büyük avantaj sağlar.

---

## 🛠️ Teknoloji Yığını (Tech Stack)

- **Backend:** FastAPI
- **Frontend:** Basit HTML/CSS + JavaScript (ileride React'e geçilecek)
- **Vector DB:** Qdrant
- **LLM API:** Google Gemini (yakında OpenAI desteği de eklenebilir)
- **Authentication:** Supabase (planlanıyor)
- **Veri İşleme:** Python + LangChain

---

## 🧩 Karşılaşılan Zorluklar

- Vektör veritabanına uygun veri örnekleri üretmek ve kategorilere doğru şekilde ayırmak zaman aldı.
- Farklı promptlara rağmen anlamlı sonuçlar verecek bir örnek yapısı kurmak zordu.
- LLM'in bazen verilen bileşenleri tam olarak takip etmemesi (hallucination riski).
- Prompt mühendisliği ile yaratıcı ama kontrollü çıktılar elde etme denemeleri zaman aldı.

---

## 🚧 Eklenecek Özellikler

- [ ] Kullanıcı girişi ve oturum yönetimi
- [ ] Vektör veritabanının daha zengin ve dengeli hale getirilmesi
- [ ] Kullanıcının kendi karakterini oluşturabilme
- [ ] Hikayeleri PDF olarak dışa aktarabilme
- [ ] Hikayelerin seslendirilmesi (TTS entegrasyonu)

