document.addEventListener('DOMContentLoaded', () => {
    // Seletores de UI (Padrão Senior)
    const elements = {
        powder: document.getElementById('coffee-powder'),
        filters: document.getElementById('filters-count'),
        daysLeft: document.getElementById('days-left'),
        rankingList: document.getElementById('ranking-list'),
        chatMessages: document.getElementById('chat-messages'),
        chatForm: document.getElementById('chat-form'),
        userInput: document.getElementById('user-input'),
        refreshBtn: document.getElementById('refresh-btn'),
        dailyPrepBtn: document.getElementById('daily-prep-btn')
    };

    // Carregar inventário inicial
    fetchInventory();

    // Event Listeners
    if (elements.refreshBtn) elements.refreshBtn.addEventListener('click', fetchInventory);
    
    if (elements.chatForm) {
        elements.chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = elements.userInput?.value.trim();
            if (!message) return;

            addMessage(message, 'user');
            if (elements.userInput) elements.userInput.value = '';
            setLoading(true);
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message })
                });
                
                if (!response.ok) throw new Error('Falha na comunicação');
                
                const data = await response.json();
                addMessage(data.reply, 'bot');
                await fetchInventory();
            } catch (error) {
                addMessage('ERRO: Terminal offline ou comando inválido.', 'bot');
            } finally {
                setLoading(false);
            }
        });
    }

    function setLoading(isLoading) {
        if (elements.userInput) elements.userInput.disabled = isLoading;
        const btn = elements.chatForm?.querySelector('.btn-send');
        if (btn) {
            btn.disabled = isLoading;
            btn.textContent = isLoading ? '...' : 'ENVIAR';
        }
    }

    if (elements.dailyPrepBtn) {
        elements.dailyPrepBtn.addEventListener('click', async () => {
            if (confirm('Deseja registrar o preparo diário? Isso subtrairá 180g de pó e 2 filtros.')) {
                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: "registre o preparo diário" })
                    });
                    const data = await response.json();
                    addMessage(data.reply, 'bot');
                    fetchInventory();
                } catch (error) {
                    alert('Erro ao registrar preparo.');
                }
            }
        });
    }

    async function fetchInventory() {
        try {
            const response = await fetch('/api/inventory');
            if (!response.ok) return;
            const data = await response.json();
            
            // Dashboard com Safe-Access
            if (elements.powder) elements.powder.textContent = data.pó;
            if (elements.filters) elements.filters.textContent = data.filtros;
            
            // Predição
            if (elements.daysLeft) {
                elements.daysLeft.textContent = data.dias_restantes;
                updatePredictionStatus(data.dias_restantes);
            }
            
            // Ranking
            if (elements.rankingList) renderRanking(data.ranking);
        } catch (error) {
            console.error('Erro de sincronização CoffeeMaster:', error);
        }
    }

    function updatePredictionStatus(days) {
        if (!elements.daysLeft) return;

        if (days <= 2) {
            elements.daysLeft.style.color = "#ff3b30"; // Vermelho Crítico
        } else if (days <= 5) {
            elements.daysLeft.style.color = "#ff9500"; // Laranja Alerta
        } else {
            elements.daysLeft.style.color = "var(--primary-color)"; // Normal
        }
    }

    function renderRanking(ranking) {
        if (!elements.rankingList) return;
        elements.rankingList.innerHTML = '';
        
        // Exibir apenas os Top 3 na UI para manter a diagramação limpa
        const top3 = ranking.slice(0, 3);
        
        top3.forEach(member => {
            const li = document.createElement('li');
            li.className = 'ranking-item';
            
            const infoDiv = document.createElement('div');
            const nameSpan = document.createElement('span');
            nameSpan.className = 'member-name';
            nameSpan.textContent = member.name;
            
            const badgeSpan = document.createElement('span');
            badgeSpan.className = 'member-badge';
            badgeSpan.textContent = member.badge;
            
            infoDiv.appendChild(nameSpan);
            infoDiv.appendChild(badgeSpan);
            
            const pointsSpan = document.createElement('span');
            pointsSpan.className = 'member-points';
            pointsSpan.textContent = `${member.points} pts`;
            
            li.appendChild(infoDiv);
            li.appendChild(pointsSpan);
            elements.rankingList.appendChild(li);
        });
    }

    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = text;
        
        messageDiv.appendChild(contentDiv);
        elements.chatMessages.appendChild(messageDiv);
        
        // Scroll Suave (Padrão Senior)
        elements.chatMessages.scrollTo({
            top: elements.chatMessages.scrollHeight,
            behavior: 'smooth'
        });

        // Acessibilidade: Anuncia nova mensagem se for do bot
        if (sender === 'bot') {
            const announcement = document.createElement('div');
            announcement.setAttribute('role', 'alert');
            announcement.setAttribute('aria-live', 'polite');
            announcement.className = 'sr-only';
            announcement.textContent = `CoffeeMaster respondeu: ${text}`;
            document.body.appendChild(announcement);
            setTimeout(() => announcement.remove(), 3000);
        }
    }
});
