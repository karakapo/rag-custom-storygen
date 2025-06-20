# 📖 Storymaker

Storymaker, yapay zeka desteğiyle çocuklara yönelik hikayeler oluşturan bir uygulamadır. İki farklı şekilde hikaye üretimi mümkündür:

1. **Serbest Mod:** Kullanıcının girdiği prompt, optimizasyondan sonra bir LLM'e (Large Language Model) gönderilir ve modelden gelen yanıt hikaye olarak sunulur.
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
- Yaratıcılığı artırır,
- Tutarlılığı korur,
- Kullanıcı girdilerini toleranslı şekilde yorumlayabilir.

Ayrıca model eğitimi gerektirmeden anlamlı çıktılar üretmeye olanak sağlar. Bu, özellikle çocuklar için içerik üretirken güvenlik ve kalite açısından büyük avantaj sağlar.

---

## 🛠️ Tech Stack

- **Backend:** FastAPI
- **Frontend:** Basit HTML/CSS + JavaScript (Yapay zeka destekli ide ile yapıldı)
- **Vector DB:** Qdrant
- **LLM API:** Google Gemini 
- **Veri İşleme:** Python + LangChain

---

## 🚀 Sistem Gelişim Süreci

- 🎯 Doğrudan LLM'e istek: Prompt direkt verildi → çıktı yüzeysel ve tutarsızdı.
- ✍️ Prompt optimizasyonu: Yapılandırılmış promptlarla kısmi iyileşme sağlandı.
- 🔍 İlk RAG denemesi: Prompt parçalanarak kategori bazlı paralel arama yapıldı → promtp parçalama zayıf kaldı.
- 🧩 Gelişmiş RAG sistemi: Prompt bütün alındı, her kategoriye ayrı arama yapıldı → çıktı tutarlı ve anlamlı hale geldi.
- 🔀 Alternatif strateji: Prompt optimizasyonu yöntemi opsiyonel bırakıldı, kullanıcı iki sistem arasında seçim yapabiliyor.

### 📈 Süreç Akışı

[Doğrudan LLM'e İstek] --> [Prompt Optimizasyonu] --> [İlk RAG Denemesi] --> [Geliştirilmiş RAG Sistemi] --> [Alternatif Strateji Eklenmesi]


---

## 🚧 Eklenecek Özellikler

- [ ] Kullanıcı girişi ve oturum yönetimi
- [ ] Vektör veritabanının daha zengin ve dengeli hale getirilmesi
- [ ] Kullanıcının kendi karakterini oluşturabilme
- [ ] Hikayeleri PDF olarak dışa aktarabilme
- [ ] Kullanıcıya özel yan karakter ekleme
- [ ] Daha test edilebilir bir yapı kurmak

---

## ⚡️ Nasıl Çalıştırılır?

### 1. Backend (FastAPI) Kurulumu ve Çalıştırılması

```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate

pip install -r requirements.txt

# Sunucuyu başlatın
uvicorn main:app --reload
```

Varsayılan olarak FastAPI backend'i `http://127.0.0.1:8000` adresinde çalışacaktır.

---

### 2. Frontend (Statik HTML/JS) Kurulumu ve Çalıştırılması

```bash
cd frontend
npm install
npm start
```

Bu komutlar, frontend'i `http://localhost:3000` adresinde başlatır.

---

### 3. Notlar

- Backend ve frontend'i aynı anda çalıştırmalısınız.
- Gerekirse `.env` dosyası ile backend ayarlarını yapabilirsiniz.
- Backend, hikaye üretimi için LLM API'lerini (ör. Google Gemini) kullanır; API anahtarınızı `.env` dosyasına eklemelisiniz.
