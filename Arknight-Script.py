
# 支持 py installer
if __name__ == '__main__':
    from module.app import create_app

    app = create_app()
    app.run(host='0.0.0.0')
