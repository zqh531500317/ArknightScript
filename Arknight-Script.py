from logzero import logger

try:
    from module.app import create_app
except Exception as e:
    logger.error(e)
app = create_app()
# 支持 py installer
if __name__ == '__main__':
    app.run(host='0.0.0.0')
