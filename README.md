# Storymaker

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