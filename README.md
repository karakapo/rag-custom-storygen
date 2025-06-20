# Storymaker 

Yapay zeka yardımıyla çocuk hikayesş yazan bri uygulama.iki farklı şekilde hikaye yazılabilir. birinci yol serbet şekilde, bu sadece llmlere request atıyor. ikinci ve yenilikçi olan yol ise rag yardımıyla hikaye yazması,önceden hazılrlanmış 8 alt katogoride (Main_character,Environment,Main_conflict,Moral,Plot,character_goal,Genre,Final_type) hazırlanan veri embdenig yapıldıktan osnra vektör db ye kayıt ediliyor. kullanıcı promtu bu vectörel dbde aratma yaprıktan sonra her katagori için anlamsal olarak en yakın 3 tane örnek allınıp bunlar arasında rastgele seçim yapılarak son hikaye yazan llm'e 8 katagoriden seçtiğimiz örenkler gönderilir ve hikaye yazılır. bunu faydası llm'e model eğitmeden daha yaratıcı şeyler üretmesini sağlamak ve çıktıyı kotrol etme şasnızı arttırmak çocuklar için yapıldığından dolayı girilen girdiyi belli oranda tolare ediebilir çünkü vektör dbdeki örenklerle sınırlı.


##Neden rag Kullandım 

##tach stack 

##projeyi yaparken yaşadığım zorluklar



##eklenecek özellikler

- [ ] Kullanıcı Giriş/Çıkış eklenecek
- [ ] Vectör Database geliştirilecek
- [ ] Kullanıcıya özel kullanıcın oluşturğu karakterler eklemecek
- [ ] 







## How to Run

### Backend

Navigate to the `backend` directory and run the application using Uvicorn:

```bash
cd backend
# Ensure you have all necessary Python packages installed (e.g., pip install -r requirements.txt if you have one)
# Make sure uvicorn is installed (e.g., pip install uvicorn)
uvicorn main:app --reload
```

### Frontend

1.  **Navigate to the `frontend` directory:**
    ```bash
    cd frontend
    ```
2.  **Open `index.html` in your web browser:**
    *   You can usually do this by double-clicking the `index.html` file.
3.  **Alternatively, use a live server (recommended for development):**
    *   If you have Node.js installed, you can use a simple HTTP server:
      ```bash
npx http-server
      ```
    *   Or, many code editors (like VS Code) have live server extensions that you can use to serve the `frontend` directory.

## Application Description

Bu uygulama, RAG (Retrieval Augmented Generation) sistemi kullanarak ve birden fazla Büyük Dil Modeli (LLM) entegre ederek çocuklar için hikayeler oluşturmayı amaçlar. RAG sisteminin kullanılmasının temel nedeni, LLM'lerin kendi başlarına sınırlı bilgiye sahip olmaları ve bu sistem sayesinde harici bir bilgi kaynağını etkin bir şekilde kullanabilmeleridir.

Uygulama, kullanıcının girdiği prompt (istek) içerisinden çeşitli hikaye bileşenlerini tanımlar. Bu bileşenler daha sonra bir vektör veritabanında aranır. Bulunan ilgili bileşenler, hikayeyi oluşturması için başka bir LLM'e girdi olarak verilir. 
