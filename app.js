const express = require('express');
const app = express();
const path = require('path');

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.use(express.static(path.join(__dirname, 'public')));
app.use(express.urlencoded({ extended: true }));

// ---- ROTAS DE LOGIN ----

app.get('/login', (req, res) => {
    res.render('login'); 
});

app.post('/auth/login', (req, res) => {
    const { usuario, senha } = req.body;
    console.log(`Tentativa de login: ${usuario}`);
    res.send(`DADOS RECEBIDOS DE ${usuario}, AGORA O BACKEND IRÁ AVALIÁ-LOS.`);
});


// ---- ROTAS DE CADASTRO ----

app.get('/cadastro', (req, res) => {
    res.render('cadastro'); 
});

app.post('/auth/cadastro', (req, res) => {
    const { nome, usuario, email, cep, senha } = req.body;
    console.log(`CADASTRO FEITO: ${usuario}`);
    res.send("CADASTRO BEM SUCEDIDO");
});


// ---- LIGA O SERVIDOR ----

app.listen(3000, () => {
    console.log("Servidor ATIVADO EM: http://localhost:3000/login");
});
