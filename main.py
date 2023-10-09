from Manager import Manager

if __name__ == "__main__":
    app=Manager()

    
    app.geometry("1000x600")
    app.columnconfigure(0, weight=1)
    app.columnconfigure(1, weight=1)
    app.mainloop()
    
    