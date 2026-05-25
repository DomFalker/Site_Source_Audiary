/* ==========================================================================
   Controles de Acessibilidade - WCAG 2 Compliance (Site Audiário)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Injetar Fonte Lexend para suporte à dislexia
    const fontLink = document.createElement('link');
    fontLink.rel = 'stylesheet';
    fontLink.href = 'https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;700&display=swap';
    document.head.appendChild(fontLink);

    // 2. Injetar Guia de Leitura (Linha horizontal)
    const guideLine = document.createElement('div');
    guideLine.id = 'reading-guide-line';
    document.body.appendChild(guideLine);

    // 3. Injetar UI do Painel de Acessibilidade
    injectAccessibilityUI();

    // 4. Inicializar Estado e Elementos
    const state = {
        fontScale: parseInt(localStorage.getItem('acc-font-scale')) || 100,
        highContrast: localStorage.getItem('acc-contrast') === 'true',
        dyslexicFont: localStorage.getItem('acc-dyslexia') === 'true',
        readingGuide: localStorage.getItem('acc-guide') === 'true'
    };

    const elements = {
        widget: document.getElementById('accessibility-widget'),
        btn: document.getElementById('accessibility-btn'),
        dialog: document.getElementById('accessibility-dialog'),
        fontDec: document.getElementById('acc-font-dec'),
        fontNormal: document.getElementById('acc-font-normal'),
        fontInc: document.getElementById('acc-font-inc'),
        contrastToggle: document.getElementById('acc-contrast-toggle'),
        dyslexiaToggle: document.getElementById('acc-dyslexia-toggle'),
        guideToggle: document.getElementById('acc-guide-toggle'),
        resetBtn: document.getElementById('acc-reset'),
        guideLine: document.getElementById('reading-guide-line')
    };

    // 5. Aplicar Estado Inicial
    applyState();

    // 6. Configurar Event Listeners de Acessibilidade Geral
    setupGeneralAccessibility();

    // 7. Configurar Event Listeners dos Controles do Painel
    setupPanelEvents();

    /* ==========================================================================
       Funções Auxiliares
       ========================================================================== */

    function injectAccessibilityUI() {
        const widgetHtml = `
            <div id="accessibility-widget" role="region" aria-label="Opções de Acessibilidade">
                <button id="accessibility-btn" aria-haspopup="dialog" aria-expanded="false" aria-label="Abrir menu de acessibilidade" title="Acessibilidade">
                    <svg viewBox="0 0 24 24" aria-hidden="true">
                        <path d="M12 2c1.1 0 2 .9 2 2s-.9 2-2 2-2-.9-2-2 .9-2 2-2zm9 7h-6v13h-2v-6h-2v6H9V9H3V7h18v2z"/>
                    </svg>
                </button>
                <div id="accessibility-dialog" role="dialog" aria-label="Menu de configurações de acessibilidade" aria-modal="false">
                    <h2>
                        <svg style="width:20px;height:20px;fill:currentColor;vertical-align:middle;margin-right:4px;" viewBox="0 0 24 24" aria-hidden="true">
                            <path d="M12 2c1.1 0 2 .9 2 2s-.9 2-2 2-2-.9-2-2 .9-2 2-2zm9 7h-6v13h-2v-6h-2v6H9V9H3V7h18v2z"/>
                        </svg>
                        Painel de Acessibilidade
                    </h2>
                    
                    <div class="acc-section">
                        <span class="acc-label" id="label-tamanho-fonte">Tamanho do Texto: <span id="font-scale-display">100%</span></span>
                        <div class="acc-btn-group" role="group" aria-labelledby="label-tamanho-fonte">
                            <button type="button" class="acc-btn" id="acc-font-dec" aria-label="Diminuir tamanho do texto">A-</button>
                            <button type="button" class="acc-btn" id="acc-font-normal" aria-label="Tamanho de texto padrão">A</button>
                            <button type="button" class="acc-btn" id="acc-font-inc" aria-label="Aumentar tamanho do texto">A+</button>
                        </div>
                    </div>

                    <div class="acc-section">
                        <div class="acc-toggle-row">
                            <span class="acc-label" id="label-alto-contraste">Alto Contraste</span>
                            <label class="acc-switch">
                                <input type="checkbox" id="acc-contrast-toggle" aria-labelledby="label-alto-contraste">
                                <span class="acc-slider"></span>
                            </label>
                        </div>
                    </div>

                    <div class="acc-section">
                        <div class="acc-toggle-row">
                            <span class="acc-label" id="label-dyslexia">Fonte para Dislexia</span>
                            <label class="acc-switch">
                                <input type="checkbox" id="acc-dyslexia-toggle" aria-labelledby="label-dyslexia">
                                <span class="acc-slider"></span>
                            </label>
                        </div>
                    </div>

                    <div class="acc-section">
                        <div class="acc-toggle-row">
                            <span class="acc-label" id="label-guide">Guia de Leitura</span>
                            <label class="acc-switch">
                                <input type="checkbox" id="acc-guide-toggle" aria-labelledby="label-guide">
                                <span class="acc-slider"></span>
                            </label>
                        </div>
                    </div>

                    <button type="button" class="acc-reset-btn" id="acc-reset" aria-label="Resetar todas as configurações de acessibilidade">
                        Restaurar Padrão
                    </button>
                </div>
            </div>
        `;
        const container = document.createElement('div');
        container.innerHTML = widgetHtml;
        document.body.appendChild(container.firstElementChild);
    }

    function applyState() {
        // A. Aplicar escala do texto
        document.documentElement.style.fontSize = `${state.fontScale}%`;
        const scaleDisplay = document.getElementById('font-scale-display');
        if (scaleDisplay) scaleDisplay.textContent = `${state.fontScale}%`;
        
        // Atualizar estado ativo dos botões de fonte
        elements.fontDec.classList.remove('active');
        elements.fontNormal.classList.remove('active');
        elements.fontInc.classList.remove('active');
        if (state.fontScale < 100) elements.fontDec.classList.add('active');
        else if (state.fontScale === 100) elements.fontNormal.classList.add('active');
        else elements.fontInc.classList.add('active');

        // B. Aplicar alto contraste
        if (state.highContrast) {
            document.body.classList.add('high-contrast');
            elements.contrastToggle.checked = true;
        } else {
            document.body.classList.remove('high-contrast');
            elements.contrastToggle.checked = false;
        }

        // C. Aplicar fonte dislexia
        if (state.dyslexicFont) {
            document.body.classList.add('dyslexic-font');
            elements.dyslexiaToggle.checked = true;
        } else {
            document.body.classList.remove('dyslexic-font');
            elements.dyslexiaToggle.checked = false;
        }

        // D. Aplicar guia de leitura
        if (state.readingGuide) {
            elements.guideLine.style.display = 'block';
            elements.guideToggle.checked = true;
        } else {
            elements.guideLine.style.display = 'none';
            elements.guideToggle.checked = false;
        }
    }

    function setupGeneralAccessibility() {
        // Detectar navegação por teclado (Tecla Tab)
        window.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                document.body.classList.add('keyboard-navigating');
            }
        });

        // Remover classe de navegação por teclado ao clicar com o mouse
        window.addEventListener('mousedown', () => {
            document.body.classList.remove('keyboard-navigating');
        });

        // Guia de leitura segue o cursor verticalmente
        window.addEventListener('mousemove', (e) => {
            if (state.readingGuide) {
                elements.guideLine.style.top = `${e.clientY - 2}px`;
            }
        });

        // Adicionar tratamento de acessibilidade para cards de categorias clicáveis na Home
        const categoryCards = document.querySelectorAll('.grid > div[class*="cursor-pointer"]');
        categoryCards.forEach(card => {
            // Se o card não tiver tabindex, adicionar
            if (!card.getAttribute('tabindex')) {
                card.setAttribute('tabindex', '0');
            }
            if (!card.getAttribute('role')) {
                card.setAttribute('role', 'button');
            }
            // Ouvir tecla Enter e Espaço para simular clique
            card.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    card.click();
                }
            });
        });
    }

    function setupPanelEvents() {
        // Alternar abertura do menu
        elements.btn.addEventListener('click', (e) => {
            const expanded = elements.btn.getAttribute('aria-expanded') === 'true';
            elements.btn.setAttribute('aria-expanded', !expanded);
            elements.dialog.classList.toggle('active');
            
            if (!expanded) {
                // Focar no primeiro item do diálogo quando abrir
                setTimeout(() => elements.fontDec.focus(), 100);
            }
        });

        // Fechar com a tecla Escape
        elements.widget.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                elements.btn.setAttribute('aria-expanded', 'false');
                elements.dialog.classList.remove('active');
                elements.btn.focus();
            }
        });

        // Fechar ao clicar fora do widget
        document.addEventListener('click', (e) => {
            if (!elements.widget.contains(e.target)) {
                elements.btn.setAttribute('aria-expanded', 'false');
                elements.dialog.classList.remove('active');
            }
        });

        // Ações de alteração de tamanho de fonte
        elements.fontDec.addEventListener('click', () => {
            state.fontScale = Math.max(80, state.fontScale - 10);
            localStorage.setItem('acc-font-scale', state.fontScale);
            applyState();
        });

        elements.fontNormal.addEventListener('click', () => {
            state.fontScale = 100;
            localStorage.setItem('acc-font-scale', state.fontScale);
            applyState();
        });

        elements.fontInc.addEventListener('click', () => {
            state.fontScale = Math.min(150, state.fontScale + 10);
            localStorage.setItem('acc-font-scale', state.fontScale);
            applyState();
        });

        // Ações de toggle
        elements.contrastToggle.addEventListener('change', (e) => {
            state.highContrast = e.target.checked;
            localStorage.setItem('acc-contrast', state.highContrast);
            applyState();
        });

        elements.dyslexiaToggle.addEventListener('change', (e) => {
            state.dyslexicFont = e.target.checked;
            localStorage.setItem('acc-dyslexia', state.dyslexicFont);
            applyState();
        });

        elements.guideToggle.addEventListener('change', (e) => {
            state.readingGuide = e.target.checked;
            localStorage.setItem('acc-guide', state.readingGuide);
            applyState();
        });

        // Ação de reset
        elements.resetBtn.addEventListener('click', () => {
            state.fontScale = 100;
            state.highContrast = false;
            state.dyslexicFont = false;
            state.readingGuide = false;

            localStorage.removeItem('acc-font-scale');
            localStorage.removeItem('acc-contrast');
            localStorage.removeItem('acc-dyslexia');
            localStorage.removeItem('acc-guide');

            applyState();
        });
    }
});
