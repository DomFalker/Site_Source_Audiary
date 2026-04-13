const express = require('express');
const app = express();
const path = require('path');

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.use(express.static(path.join(__dirname, 'public')));
app.use(express.urlencoded({ extended: true }));

//---- ROTA HOME ----
app.get('/', (req, res) => {
    res.render('index');
});

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
    const { nome, usuario, email, cep, rua, senha } = req.body;
    console.log(`CADASTRO FEITO: ${usuario}`);
    console.log('NO ENDEREÇO ${rua}');
    res.send("CADASTRO BEM SUCEDIDO");
});

// ---- ROTA PARA RECUPERAR SENHA PERDIDA ----
app.get('/senha-esquecida', (req, res) => {
    res.render('senha-esquecida');
});

app.post('/auth/recuperar-senha', (req, res) => {
    const{ email } = req.body;
    res.send(`Um link de recuperação foi enviado para ${email}`);

    //Resposta esperar para o backend hihiihihihi
    res.send('Um link de recuperação já foi enviado para ${email} esquecidinho!');
});

// ---- ROTA DA VITRINE ----

app.get('/produtos', (req, res) => {
    res.render('produtos');
});

// ---- LIGA O SERVIDOR ----

app.listen(3000, () => {
    console.log("Servidor ATIVADO EM: http://localhost:3000/login");
});
