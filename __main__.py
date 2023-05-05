r"""
top-level package interface of this project

- `\UwU> python .`
- `\UwU\..> python UwU`
"""
import multiprocessing
import uvicorn


# run the FastAPI server
multiprocessing.Process(
    target=uvicorn.run, 
    args=('app.api:web',),
    kwargs={'reload': True}
).start()

# run the Tkinter GUI
multiprocessing.Process(
    target=__import__, 
    args=('app.interface',)
).start()