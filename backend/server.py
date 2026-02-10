if __name__ == "__main__":
    import uvicorn
    # import os
    # port = int(os.environ.get("PORT", 80)) ## Deploying to render
    uvicorn.run("server:app", host="127.0.0.1", port=8080, reload=True)