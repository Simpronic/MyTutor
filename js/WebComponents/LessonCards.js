class LessonCard extends HTMLElement {
  static get observedAttributes() {
    return ['id','title', 'name', 'first', 'last', 'subject', 'topics', 'variant', 'href', 'button-text','date'];
  }

  connectedCallback() {
    this.render();
    this.attachButtonHandler();
  }

  attributeChangedCallback() {
    this.render();
    this.attachButtonHandler();
  }

  getAttr(name, fallback = '') {
    const v = this.getAttribute(name);
    return v === null ? fallback : v;
  }

  render() {
    const title = this.getAttr('title', '');
    const name =
      this.getAttr('name', '').trim() ||
      `${this.getAttr('first', '').trim()} ${this.getAttr('last', '').trim()}`.trim();

    const subject = this.getAttr('subject', '');
    const topics = this.getAttr('topics', '');
    const variant = this.getAttr('variant', 'event'); // event -> .event-card, lesson -> .lesson-card
    const href = this.getAttr('href', '');
    const buttonText = this.getAttr('button-text', 'Informazioni');
    const date = this.getAttr('date','')

    this.innerHTML = `
      <div class="card ${variant}-card text-center w-100 h-100">
        <div class="card-body">
          ${title ? `<h6 class="card-title text-primary">${title}</h6>` : ''}
          ${name ? `<h5 class="card-title">${name}</h5>` : ''}
          ${subject ? `<p class="card-text">Materie: ${subject}</p>` : ''}
          ${topics ? `<p class="card-text">Argomenti: ${topics}</p>` : ''}
          ${date ? `<p class="card-text">Data: ${date}</p>` : ''}

          <button class="btn btn-primary btn-sm mt-2" type="button" data-href="${href}">
            ${buttonText}
          </button>
        </div>
      </div>
    `;
  }

  attachButtonHandler() {
    const btn = this.querySelector('button');
    if (!btn) return;
    btn.onclick = null;
    btn.onclick = () => {
      alert(this.getAttr('id'))
      const href = btn.dataset.href;
      if (href) window.location.href = href;
      else this.dispatchEvent(new CustomEvent('lesson-open', { bubbles: true }));
    };
  }
}

customElements.define('lesson-card', LessonCard);
