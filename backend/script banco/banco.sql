CREATE DATABASE IF NOT EXISTS empresa_inseminacao;
USE empresa_inseminacao;

-- Tabela de Fazendas
CREATE TABLE fazendas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_fazenda VARCHAR(100),
    estado VARCHAR(50),
    municipio VARCHAR(100)
);

-- Tabela de vacas
CREATE TABLE vacas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_fazenda INT,
    numero_animal INT,
    lote VARCHAR(50),
    vaca VARCHAR(50),
    categoria VARCHAR(50),
    ECC FLOAT,
    ciclicidade INT,
    FOREIGN KEY (id_fazenda) REFERENCES fazendas(id)
);

-- Tabela de Protocolos de Inseminação
CREATE TABLE protocolos_inseminacao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    protocolo VARCHAR(100),
    dias_protocolo INT,
    implante_P4 VARCHAR(100),
    empresa VARCHAR(100),
    GnRH_NA_IA TINYINT,
    PGF_NO_D0 INT,
    dose_PGF_retirada DECIMAL(10,2),
    marca_PGF_retirada VARCHAR(100),
    dose_CE DECIMAL(10,2),
    eCG VARCHAR(100),
    dose_eCG DECIMAL(10,2)
);

-- Tabela de Inseminadores
CREATE TABLE inseminadores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_inseminador VARCHAR(100)
);

-- Tabela de Touros
CREATE TABLE touros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_touro VARCHAR(100),
    raca_touro VARCHAR(50),
    empresa_touro VARCHAR(100)
);

-- Tabela de Clientes (Fazendas)
CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_fazenda INT,
    nome_cliente VARCHAR(100),
    email VARCHAR(100),
    telefone VARCHAR(20),
    endereco VARCHAR(200),
    FOREIGN KEY (id_fazenda) REFERENCES fazendas(id)
);

-- Tabela de Vendas
CREATE TABLE vendas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    data_venda DATE,
    valor_total DECIMAL(10, 2),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id)
);


-- Tabela de Resultados de Inseminação
CREATE TABLE resultados_inseminacao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_vaca INT,
    id_protocolo INT,
    id_touro INT,
    id_inseminador INT,
    id_venda INT,
    data_inseminacao DATE,
    numero_IATF VARCHAR(100),
    DG TINYINT,
    vazia_Com_Ou_Sem_CL tinyint,
    perda TINYINT,
    FOREIGN KEY (id_vaca) REFERENCES vacas(id),
    FOREIGN KEY (id_protocolo) REFERENCES protocolos_inseminacao(id),
    FOREIGN KEY (id_touro) REFERENCES touros(id),
    FOREIGN KEY (id_inseminador) REFERENCES inseminadores(id),
    FOREIGN KEY (id_venda) REFERENCES vendas(id)
);

-- Tabela de Produtos
CREATE TABLE produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_produto VARCHAR(100),
    descricao TEXT,
    preco_unitario DECIMAL(10, 2)
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE chats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(40) NOT NULL,
    user_id INT NOT NULL,
    id_gpt TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text_usuario TEXT NOT NULL,
    text_servidor TEXT NOT NULL,
    chat_id INT NOT NULL,
    FOREIGN KEY (chat_id) REFERENCES chats(id)
);

CREATE TABLE visitas(
    id int AUTO_INCREMENT PRIMARY KEY,
    id_fazenda int NOT NULL,
    data_visita date NOT NULL,
    FOREIGN KEY (id_fazenda) REFERENCES fazendas(id)
);

INSERT INTO fazendas (nome_fazenda, estado, municipio) VALUES
('Fazenda Marajoara', 'TO', 'CARIRI DO TOCANTINS'),
('Fazenda Exemplo', 'SP', 'Assis'),
('Fazenda Boa Vista', 'MG', 'Uberaba'),
('Fazenda São João', 'GO', 'Rio Verde'),
('Fazenda Sol Nascente', 'BA', 'Barreiras'),
('Fazenda Boa Esperança', 'MS', 'Campo Grande'),
('Fazenda Santa Rita', 'MT', 'Cuiabá'),
('Fazenda Paraíso', 'PR', 'Londrina'),
('Fazenda São Francisco', 'RS', 'Porto Alegre'),
('Fazenda Bela Vista', 'SC', 'Chapecó'),
('Fazenda Primavera', 'SP', 'Ribeirão Preto'),
('Fazenda Esperança', 'SP', 'Bauru'),
('Fazenda Céu Azul', 'GO', 'Goiânia');

INSERT INTO vacas (id_fazenda, numero_animal, lote, vaca, categoria, ECC, ciclicidade) VALUES
(1, 112349, 'LT01MRJ', 'Nelore', 'Multípara', 3, 0),
(2, 178423, 'LT02EX', 'Angus', 'Multípara', 3.5, 1),
(3, 333423, 'LT03BV', 'Guzerá', 'Nulípara', 3, 0),
(4, 446753, 'LT04SJ', 'Gir Leiteiro', 'Multípara', 2.75, 1),
(5, 559023, 'LT05SN', 'Simental', 'Primípara tardia', 4, 0),
(6, 678431, 'LT06BE', 'Charolês', 'Multípara', 3.75, 1),
(7, 700940, 'LT07SR', 'Brahman', 'Primípara precoce', 2.5, 1),
(8, 809843, 'LT08PS', 'Angus', 'Multípara', 3.25, 1),
(9, 994758, 'LT09SF', 'Hereford', 'Nulípara', 3.5, 1),
(10, 109384, 'LT10BV', 'Bonsmara', 'Primípara precoce', 3, 1),
(11, 119011, 'LT11PV', 'Girolando', 'Secundípara', 2.75, 1),
(12, 149820, 'LT14EP', 'Holandesa', 'Primípara precoce', 3.25, 1),
(13, 151423, 'LT15CA', 'Tabapuã', 'Primípara tardia', 3.5, 1);

INSERT INTO protocolos_inseminacao (protocolo, dias_protocolo, implante_P4, empresa, GnRH_NA_IA, PGF_NO_D0, dose_PGF_retirada, marca_PGF_retirada, dose_CE, eCG, dose_eCG) VALUES
('9 dias', 9, 'Fertilcare 600', 'MSD', 0, 0, 1.1, 'Ciosin', 0.5, 'Folligon', 300),
('7 dias', 7, 'CIDR', 'Zoetis', 1, 1, 2.1, 'Prostagland', 0.8, 'eCGEN', 250),
('10 dias', 10, 'Sincrogest', 'Ourofino', 0, 0, 1.1, 'Sincrogest', 1.0, 'Folltropin', 350),
('7 dias', 7, 'ReproGest', 'Biogénesis Bagó', 1, 1, 2.1, 'Reprosinc', 0.7, 'eCGEN', 300),
('9 dias', 9, 'CIDR', 'Zoetis', 0, 0, 1.1, 'Sincropart', 0.6, 'Folltropin', 250),
('8 dias', 8, 'Syncro-mate B', 'Syntex', 1, 1, 2.1, 'Prostagland', 0.7, 'eCGEN', 300),
('10 dias', 10, 'Repro one', 'Globalgen', 1, 1, 1.1, 'Induscio', 0.8, 'Novormon', 250),
('8 dias', 8, 'Syncro-mate B', 'Syntex', 1, 1, 2.1, 'Prostagland', 0.6, 'eCGEN', 200),
('9 dias', 9, 'CIDR', 'Zoetis', 1, 1, 2.1, 'Estron', 0.5, 'eCGEN', 250),
('7 dias', 7, 'Primer monodose', 'Agener', 1, 1, 2.1, 'Estron', 0.8, 'eCGEN', 300),
('8 dias', 8, 'Repro one', 'Globalgen', 1, 1, 1.1, 'Induscio', 0.7, 'Folligon', 300),
('8 dias', 8, 'Repro one', 'Globalgen', 1, 1, 1.1, 'Induscio', 0.7, 'Folligon', 300);

INSERT INTO inseminadores (nome_inseminador) VALUES
('Rafael'),
('Bruna'),
('Henrique'),
('Carlos'),
('Daniela'),
('Felipe'),
('James'),
('Karla'),
('Marcos'),
('Jader'),
('Bernardo'),
('Josafá'),
('Daniel');

INSERT INTO touros (nome_touro, raca_touro, empresa_touro) VALUES
('Nelore', 'Nelore', 'ABS Pecplan'),
('Hereford', 'Angus', 'Genex'),
('Tabapuã', 'Tabapuã', 'ABS Pecplan'),
('Sindi', 'Nelore', 'Semex'),
('Girolando', 'Girolando', 'ABS Pecplan'),
('Limousin', 'Limousin', 'CRV Lagoa'),
('Bonsmara', 'Bonsmara', 'Genex'),
('Red Angus', 'Angus', 'Genex'),
('Charolês', 'Charolês', 'ABS Pecplan'),
('Angus', 'Angus', 'Genex'),
('Nelore', 'Nelore', 'CRV Lagoa'),
('Holandês', 'Holandês', 'CRV Lagoa'),
('Nelore', 'Nelore', 'ABS Pecplan');

INSERT INTO clientes(id_fazenda, nome_cliente, email, telefone, endereco) VALUES
(1, 'Cliente 1', 'cliente1@example.com', '123456789', 'Endereço do Cliente 1'),
(2, 'Cliente 2', 'cliente2@example.com', '123456789', 'Endereço do Cliente 2'),
(3, 'Cliente 3', 'cliente3@example.com', '123456789', 'Endereço do Cliente 3'),
(4, 'Cliente 4', 'cliente4@example.com', '123456789', 'Endereço do Cliente 4'),
(5, 'Cliente 5', 'cliente5@example.com', '123456789', 'Endereço do Cliente 5'),
(6, 'Cliente 6', 'cliente6@example.com', '123456789', 'Endereço do Cliente 6'),
(7, 'Cliente 7', 'cliente7@example.com', '123456789', 'Endereço do Cliente 7'),
(8, 'Cliente 8', 'cliente8@example.com', '123456789', 'Endereço do Cliente 8'),
(9, 'Cliente 9', 'cliente9@example.com', '123456789', 'Endereço do Cliente 9'),
(10, 'Cliente 10', 'cliente10@example.com', '123456789', 'Endereço do Cliente 10'),
(11, 'Cliente 11', 'cliente11@example.com', '123456789', 'Endereço do Cliente 11'),
(12, 'Cliente 12', 'cliente12@example.com', '123456789', 'Endereço do Cliente 12'),
(13, 'Cliente 13', 'cliente13@example.com', '123456789', 'Endereço do Cliente 13');

INSERT INTO vendas (id_cliente, data_venda, valor_total) VALUES
(1, '2024-01-01', 1000.00),
(2, '2024-01-02', 1500.00),
(3, '2024-01-03', 2000.00),
(4, '2024-01-04', 2500.00),
(5, '2024-01-05', 3000.00),
(6, '2024-01-06', 3500.00),
(7, '2024-01-07', 4000.00),
(8, '2024-01-08', 4500.00),
(9, '2024-01-09', 5000.00),
(10, '2024-01-10', 5500.00),
(11, '2024-01-11', 6000.00),
(12, '2024-01-12', 6500.00),
(13, '2024-01-13', 7000.00);

INSERT INTO resultados_inseminacao (id_vaca, id_protocolo, id_touro, id_inseminador, id_venda, data_inseminacao, numero_IATF, DG, vazia_Com_Ou_Sem_CL, perda) VALUES
(1, 1, 1, 1, 1, '2024-01-15', 'IATF 1', 1, 1, 1),
(2, 2, 2, 2, 2, '2024-01-16', 'IATF 3', 1, 0, 0),
(3, 3, 3, 3, 3, '2024-01-17', 'IATF 4', 1, 1, 0),
(4, 4, 4, 4, 4, '2024-01-18', 'IATF 5', 0, 0, 1),
(5, 5, 5, 5, 5, '2024-01-19', 'IATF 6', 1, 1, 0),
(6, 6, 6, 6, 6, '2024-01-20', 'IATF 7', 0, 0, 0),
(7, 7, 7, 7, 7, '2024-01-21', 'IATF 8', 1, 0, 0),
(8, 8, 8, 8, 8, '2024-01-22', 'IATF 9', 0, 0, 1),
(9, 9, 9, 9, 9, '2024-01-23', 'IATF 10', 1, 0, 0),
(10, 10, 10, 10, 10, '2024-01-24', 'IATF 11', 0, 0, 1),
(11, 11, 11, 11, 11, '2024-01-25', 'IATF 12', 1, 0, 1),
(12, 12, 12, 12, 12, '2024-01-26', 'IATF 15', 1, 0, 1),
(13, 1, 13, 13, 13, '2024-01-27', 'IATF 16', 0, 0, 1);

INSERT INTO produtos (nome_produto, descricao, preco_unitario) VALUES
('Produto 1', 'Descrição do Produto 1', 10.50),
('Produto 2', 'Descrição do Produto 1', 11.00),
('Produto 3', 'Descrição do Produto 1', 12.50),
('Produto 4', 'Descrição do Produto 1', 13.00);

INSERT INTO visitas (id_fazenda, data_visita) VALUES
(1, '2024-01-15'),
(1, '2024-04-15'),
(1, '2024-03-15'),
(2, '2024-02-10'),
(2, '2024-05-10'),
(2, '2024-01-10'),
(3, '2024-02-10'),
(3, '2024-05-10'),
(3, '2024-01-10'),
(4, '2024-02-10'),
(4, '2024-05-10'),
(4, '2024-01-10'),
(5, '2024-02-10'),
(5, '2024-05-10'),
(5, '2024-01-10');