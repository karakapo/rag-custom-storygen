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

## 🚀 Sistem Gelişim Süreci

### 1. 🎯 Doğrudan LLM'e İstek Gönderme
- Kullanıcıdan alınan prompt doğrudan LLM'e verildi.
- **Sonuç:** Üretilen hikâyeler yüzeyseldi, anlam ve yapı açısından zayıftı.

---

### 2. ✍️ Prompt Optimizasyonu
- Prompt yapısı kurallara göre yeniden biçimlendirildi ve LLM'e iletildi.
- **İyileşme:** Dilsel kalite kısmen arttı, ama derinlik hâlâ sınırlıydı.

---

### 3. 🔍 İlk RAG Denemesi
- Prompt’tan tematik kategoriler (karakter, mekân, tema vs.) çıkarıldı.
- Bu parçalar ayrı ayrı vektör veritabanında aratıldı.
- **Problem:** Prompt'tan doğru kategori bilgisi çıkarımı zayıftı → sonuçlar alakasızlaştı.

---

### 4. 🧩 Geliştirilmiş RAG Sistemi
- Prompt olduğu gibi kullanıldı; her kategori için **ayrı arama** yapıldı.
- **Sonuç:** Her parça kendi semantik bağlamında içerik getirdi, hikâyeler çok daha tutarlı ve anlamlı hale geldi.

---

### 5. 🔀 Alternatif Strateji Eklenmesi
- İlk (kategori çıkarımlı) yaklaşım ikinci seçenek olarak sistemde tutuldu.
- Kullanıcıya iki strateji sunuldu:
  - ✅ Tam prompt + çoklu kategori araması *(varsayılan ve güçlü sistem)*
  - 🧪 Parçalı kategori çıkarımı + arama *(alternatif yöntem)*

---

## 📈 Süreç Akışı

```mermaid
graph TD
    A[Doğrudan LLM'e İstek] --> B[Prompt Optimizasyonu]
    B --> C[İlk RAG Denemesi]
    C --> D[Geliştirilmiş RAG Sistemi]
    D --> E[Alternatif Strateji Eklenmesi]


---

## 🚧 Eklenecek Özellikler

- [ ] Kullanıcı girişi ve oturum yönetimi
- [ ] Vektör veritabanının daha zengin ve dengeli hale getirilmesi
- [ ] Kullanıcının kendi karakterini oluşturabilme
- [ ] Hikayeleri PDF olarak dışa aktarabilme

