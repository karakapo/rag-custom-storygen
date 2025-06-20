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
- **Frontend:** Basit HTML/CSS + JavaScript (Yapay zeka destekli ide ile yapıldı)
- **Vector DB:** Qdrant
- **LLM API:** Google Gemini 
- **Veri İşleme:** Python + LangChain

---

## 🧩 Karşılaşılan Zorluklar
## proje aşamaları 
- llm'e istek gönderek
    - bu fazla basit ve yüzeysel hikayeler yazıyordu
- promt omptimzations
    - kullanıcıdan alınan promtu optimize edip yine llme vermeyi denedim kayda değer bir değişiklik olmadı ama ilk halinden iyiydi
- İlk rag denemesi
     -her bir promtun içinden önceden belirlenen katogoriler çıkartırlıp vectör dbde aranması, parelel search ile . burda promttan katagori içeriklerini çıkama işemi yeterince iyi çalışmadı
- Rag- Bütün promtu alıp bütün katogorilerde ayrı ayrı serach yapamak ve 2.sıradaki sistemide seçenek olarak eklemek
    - üsteki şeyi açıkla


## 🚀 Proje Gelişim Süreci

1️⃣ **Doğrudan LLM'e İstek Gönderme**  
➡️  
- Kullanıcı promptu doğrudan LLM'e gönderiliyordu.  
- ✔️ Basit bir başlangıç sağladı.  
- ❌ Ancak sonuçlar yüzeysel, tutarsız ve yaratıcılıktan uzaktı.

---

2️⃣ **Prompt Optimizasyonu**  
➡️  
- Kullanıcıdan alınan girdilere yapısal eklemeler yapılarak LLM’e daha zengin promptlar verildi.  
- ✔️ Tutarlılık az da olsa arttı.  
- ❌ Fakat içerik hâlâ sınırlı düzeyde gelişmişti. Beklenen etkiyi yaratmadı.

---

3️⃣ **İlk RAG Denemesi**  
➡️  
- Promptun içinden 8 kategoriye ait içerikleri ayıklayıp, her birini ayrı ayrı vektör veritabanında aratmak hedeflendi.  
- ✔️ Kategori bazlı yapı kurulmaya başlandı.  
- ❌ Ancak prompttan anlamlı kategori çıkarımı istikrarsızdı.  
- ❌ Sistem kararsız çalıştı, hataya çok açıktı.

---

4️⃣ **Geliştirilmiş RAG Sistemi**  
➡️  
- Artık kullanıcı promptu bütün olarak alınarak, her bir kategori için **bağımsız semantik arama** yapılmaya başlandı.  
- ✔️ Parçalama hataları ortadan kalktı.  
- ✔️ Tutarlılık ve kontrol seviyesi ciddi oranda arttı.  
- ✔️ Her kategori için vektör veritabanından en yakın 3 örnek alınıp biri rastgele seçildi.  
- ➕ Önceki sistem (prompt parçalama) de alternatif olarak korunarak çoklu strateji geliştirildi.

---

🟢 **Sonuç:**
- Model eğitimi yapmadan yaratıcı ve kontrollü hikaye üretimi mümkün hâle geldi.
- RAG sistemi ile hem esneklik hem yapılandırılmış çıktı sağlandı.


---

## 🚧 Eklenecek Özellikler

- [ ] Kullanıcı girişi ve oturum yönetimi
- [ ] Vektör veritabanının daha zengin ve dengeli hale getirilmesi
- [ ] Kullanıcının kendi karakterini oluşturabilme
- [ ] Hikayeleri PDF olarak dışa aktarabilme

