import httpProxy from 'http-proxy';

const { createProxyServer } = httpProxy;

const proxy = createProxyServer({
    host: 'http://127.0.0.1',
    port: 5000,
    secure: false,
    changeOrigin: true,
});

const proxyMiddleWare = (req, res, next) => {
    proxy.web(req, res, { target: 'http://127.0.0.1:5000/' }, next);
};

export default proxyMiddleWare;
