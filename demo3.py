import threading

import webview


def background_task(window):
    """一个在后台运行的Python函数，可以与JS交互"""
    # time.sleep(5)
    # window.evaluate_js('alert("Python在5秒后向你问好！");')


if __name__ == "__main__":
    window = webview.create_window(
        "PyWebview 示例",
        "https://www.1lou.me",
    )
    # 启动后台线程
    thread = threading.Thread(target=background_task, args=(window,))
    thread.start()
    webview.start()
