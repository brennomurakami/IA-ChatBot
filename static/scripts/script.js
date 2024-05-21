// script.js
async function sendUserMessage() {
  const messageTextarea = document.getElementById("message");
  const messageContainer = document.getElementById("message-container");
  const userMessage = messageTextarea.value;

  if (userMessage.trim() === "") return;

  // Obtém o chat ativo
  const activeChat = document.querySelector(".chat-card.active");
  let chatId = null;

  if (activeChat) {
    chatId = activeChat.dataset.chatId;
  } else {
    // Se não houver chat ativo, cria um novo chat
    const response = await fetch("/add_chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ title: "Novo Chat" }),
    });

    if (response.ok) {
      const chatData = await response.json();
      createChatCard(chatData, chatData.chat_id);
      chatId = chatData.chat_id;
    } else {
      console.error("Erro ao adicionar chat:", response.statusText);
      return;
    }
  }

  // Limpa o textarea
  messageTextarea.value = "";

  // Cria um elemento de parágrafo para a mensagem do usuário
  const userMessageParagraph = document.createElement("p");
  userMessageParagraph.innerHTML = userMessage;
  userMessageParagraph.classList.add("message", "user-message");
  messageContainer.appendChild(userMessageParagraph); // Modificado para adicionar no 'message-container'

  // Adiciona mensagem de "aguardando resposta"
  const waitingMessageParagraph = document.createElement("p");
  waitingMessageParagraph.textContent = "Aguardando resposta do servidor, por favor aguarde...";
  waitingMessageParagraph.classList.add("message", "server-message");
  messageContainer.appendChild(waitingMessageParagraph);

  // Envia a mensagem do usuário para o servidor usando fetch
  const response = await fetch(`/get_response/${chatId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message: userMessage }),
  });

  if (!response.ok) {
    console.error("Erro ao enviar mensagem:", response.statusText);
    return;
  }

  // Remove mensagem de "aguardando resposta"
  messageContainer.removeChild(waitingMessageParagraph);

  const serverResponse = await response.json();
  serverResponse.message = marked.parse(serverResponse.message);

  const serverResponseParagraph = document.createElement("p");
  serverResponseParagraph.innerHTML = serverResponse.message;
  serverResponseParagraph.classList.add("message", "server-message");
  messageContainer.appendChild(serverResponseParagraph);

  messageContainer.scrollTop = messageContainer.scrollHeight;
}

async function updateMessageContainer(chatId) {
  try {
    // Faz uma solicitação para a rota do Flask que retorna as mensagens do chat
    const response = await fetch(`/get_messages/${chatId}`);

    if (response.ok) {
      // Extrai as mensagens do corpo da resposta
      const messages = await response.json();

      // Adiciona as mensagens ao container de mensagens
      const messageContainer = document.getElementById("message-container");
      messageContainer.innerHTML = ""; // Limpa o container de mensagens

      messages.forEach(message => {
        // Cria um elemento de parágrafo para a mensagem do usuário
        const userMessageParagraph = document.createElement("p");
        userMessageParagraph.innerHTML = message.usuario;
        userMessageParagraph.classList.add("message", "user-message");
        messageContainer.appendChild(userMessageParagraph); // Modificado para adicionar no 'message-container'

        // Cria um elemento de parágrafo para a resposta do servidor
        const serverResponseParagraph = document.createElement("p");
        serverResponseParagraph.innerHTML = marked.parse(message.servidor);
        serverResponseParagraph.classList.add("message", "server-message");
        messageContainer.appendChild(serverResponseParagraph); // Modificado para adicionar no 'message-container'
      });

      console.log("Mensagens do chat atualizadas com sucesso:", messages);
    } else {
      console.error("Erro ao obter as mensagens do chat:", response.statusText);
    }
  } catch (error) {
    console.error("Erro ao atualizar o container de mensagens:", error);
  }
}

// Função para criar um novo chat card
function createChatCard(chatData, id) {
  // Cria um novo card
  var chatCard = document.createElement("div");
  const chatList = document.getElementById("chat-list");
  var chatCards = document.querySelectorAll(".chat-card");
  chatCard.classList.add("chat-card");
  chatCard.setAttribute("data-chat-id", id); // Define o ID do chat como um atributo de dados
  chatCard.innerHTML = `
        <div class="chat-info">
            <input type="text" class="chat-name" value="${chatData.title}" disabled>
            <div class="chat-actions">
                <button class="edit-button"><i class="fas fa-edit"></i></button>
                <button class="share-button"><i class="fas fa-share"></i></button>
                <button class="delete-button"><i class="fas fa-trash-alt"></i></button>
            </div>
        </div>
    `;
  // Adiciona o card à lista de chats
  const messageContainer = document.getElementById("message-container");
  messageContainer.innerHTML = ""; // Limpa o container de mensagens
  
  chatList.appendChild(chatCard);
  chatCards = document.querySelectorAll(".chat-card");
  chatCards.forEach(function (chatCard) {
    console.log(chatCard);
    chatCard.classList.remove("active");
  });
  chatCard.classList.add("active");

  const deleteButton = chatCard.querySelector('.delete-button');
  const editButton = chatCard.querySelector('.edit-button');
  const chatNameInput = chatCard.querySelector('.chat-name');

  chatCard.addEventListener("click", function (event) {
    // Verifica se o clique ocorreu em um botão dentro do card
    if (!event.target.closest(".chat-actions")) {

      // Remove a classe "active" de todos os cards de chat
      chatCards.forEach(function (chatCard) {
        console.log(chatCard);
        chatCard.classList.remove("active");
      });

      // Adiciona a classe "active" ao card clicado
      chatCard.classList.add("active");
      console.log(chatCard);


      // Obtém o ID do chat a partir do atributo de dados
      const chatId = chatCard.getAttribute('data-chat-id');

      // Atualiza o container de mensagens com as mensagens do chat selecionado
      updateMessageContainer(chatId);
    }
  });

  deleteButton.addEventListener('click', async function (event) {
    event.preventDefault();

    const chatId = chatCard.getAttribute('data-chat-id'); // Obtenha o ID do chat

    await fetch(`/delete_chat/${chatId}`, { // Altere a URL para a sua rota de exclusão
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(),
    });
    if(chatCard.classList.contains("active")){
      const messageContainer = document.getElementById("message-container");
      messageContainer.innerHTML = ""; // Limpe o container de mensagens
    }
    chatCard.remove(); // Remova o chat-card da DOM
  });

  editButton.addEventListener('click', function () {
    chatNameInput.disabled = !chatNameInput.disabled;
    if (!chatNameInput.disabled) {
      chatNameInput.focus();
    }
  });

  // Adiciona um evento de foco ao input do nome do chat
  chatNameInput.addEventListener('blur', function () {
    chatNameInput.disabled = true;

    // Chama a função para atualizar o título do chat
    const chatId = chatCard.getAttribute('data-chat-id');
    const newTitle = chatNameInput.value;
    updateChatTitle(newTitle, chatId)
  });
}

document.addEventListener("DOMContentLoaded", function () {
  var sidebar = document.getElementById("slide-bar");
  var sidebarToggleButton = document.getElementById("sidebar-toggle-button");
  var chatList = document.getElementById("chat-list");
  var icon = document.getElementById("sidebar-toggle-icon");
  var chatCards = document.querySelectorAll(".chat-card");

  // Evento para adicionar um novo chat
  document.getElementById("add-chat-button").addEventListener("click", async function () {
    // Cria um novo chat a partir do banco de dados
    const response = await fetch("/add_chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ title: "Novo Chat" }), // Você pode enviar o título do chat aqui
    });

    if (response.ok) {
      // Obtém os dados do novo chat adicionado
      const chatData = await response.json();
      console.log(chatData)
      // Cria o card do chat com os dados obtidos
      createChatCard(chatData, chatData.chat_id);
    } else {
      console.error("Erro ao adicionar chat:", response.statusText);
    }
  });

  //Logout
  document.getElementById("logout-button").addEventListener("click", async function () {
    try {
      const response = await fetch("/logout", {
        method: "GET",
      });
  
      if (response.ok) {
        // Redireciona o usuário para a página de login ou outra página de sua escolha
        window.location.href = "/";  // Redireciona para a página de login
      } else {
        console.error("Erro ao fazer logout:", response.statusText);
      }
    } catch (error) {
      console.error("Erro ao fazer logout:", error);
    }
  });

  // Evento de clique no botão de alternância da barra lateral
  sidebarToggleButton.addEventListener("click", function () {
    sidebar.classList.toggle("open");
    sidebarToggleButton.classList.toggle("open"); // Adiciona ou remove a classe "open" do botão

    // Verifica se a barra lateral está aberta ou fechada e alterna o ícone correspondente
    if (sidebar.classList.contains("open")) {
      icon.classList.remove("fa-chevron-right");
      icon.classList.add("fa-chevron-left");
    } else {
      icon.classList.remove("fa-chevron-left");
      icon.classList.add("fa-chevron-right");
    }
  });

  // Adiciona um evento de clique a cada card
  chatCards.forEach(function (card) {
    const deleteButton = card.querySelector('.delete-button');
    const editButton = card.querySelector('.edit-button');
    const chatNameInput = card.querySelector('.chat-name');

    card.addEventListener("click", function (event) {
      // Verifica se o clique ocorreu em um botão dentro do card
      if (!event.target.closest(".chat-actions")) {

        // Remove a classe "active" de todos os cards de chat
        chatCards.forEach(function (card) {
          card.classList.remove("active");
        });

        // Adiciona a classe "active" ao card clicado
        card.classList.add("active");

        // Obtém o ID do chat a partir do atributo de dados
        const chatId = card.dataset.chatId;

        // Atualiza o container de mensagens com as mensagens do chat selecionado
        updateMessageContainer(chatId);
      }
    });

    deleteButton.addEventListener('click', async function (event) {
      event.preventDefault();

      const chatId = card.getAttribute('data-chat-id'); // Obtenha o ID do chat

      await fetch(`/delete_chat/${chatId}`, { // Altere a URL para a sua rota de exclusão
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(),
      });

      card.remove(); // Remova o chat-card da DOM
    });

    editButton.addEventListener('click', function () {
      chatNameInput.disabled = !chatNameInput.disabled;
      if (!chatNameInput.disabled) {
        chatNameInput.focus();
      }
    });

    // Adiciona um evento de foco ao input do nome do chat
    chatNameInput.addEventListener('blur', function () {
      chatNameInput.disabled = true;

      // Chama a função para atualizar o título do chat
      const chatId = card.getAttribute('data-chat-id');
      const newTitle = chatNameInput.value;
      updateChatTitle(newTitle, chatId);
    });

  });

});

async function updateChatTitle(newTitle, chatId) {
  try {
    await fetch(`/update_chat_title/${chatId}`, { // Altere a URL para a sua rota de exclusão
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ title: newTitle }),
    });
  } catch (error) {
    console.error("Erro ao enviar a solicitação de atualização do título do chat:", error);
  }
}

document.getElementById('file-span').addEventListener('click', function() {
  // Clica no elemento 'file-input' para abrir a caixa de diálogo de seleção de arquivo
  document.getElementById('file-input').click();
});
document.getElementById('file-input').addEventListener('change', function(event) {
  const file = event.target.files[0];  // Obtém o arquivo selecionado

  // Crie um objeto FormData para enviar o arquivo
  const formData = new FormData();
  formData.append('file', file);

  // Envie o arquivo para o servidor Flask usando Fetch
  fetch('/upload-arquivo', {
      method: 'POST',
      body: formData
  })
  .then(response => {
      if (!response.ok) {
          throw new Error('Erro ao enviar o arquivo.');
      }
      return response.text();
  })
  .then(data => {
      console.log(data); // Log da resposta do servidor
      // Faça qualquer outra coisa que você queira fazer após enviar o arquivo
  })
  .catch(error => {
      console.error('Erro:', error);
  });
});