class Menu extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `
            <link rel="stylesheet" href="./res/css/hamburger.css">
            <section class="wrapper">
                <section class="material-design-hamburger">
                    <button class="material-design-hamburger__icon">
                        <span class="material-design-hamburger__layer"></span>
                    </button>
                </section>
                <section class="menu menu--off">
                    <div id="view1"><a href="historic.html">Historic</a></div>
                    <div id="view2"><a href="riepilogo-partenze.html">Riepilogo Partenze</a></div>
                    <div id="view3"><a href="download.html">Download</a></div>
                    <div id="view4">
                    <div class="dropdown">
                    <button class="dropdown-toggle">Invoicing</button>
                    <div class="dropdown-menu">
                      <a href="retail_handling.html">- Retail Handling</a>
                      <a href="domestic_linehaul.html">- Domestic Linehaul</a>
                      <a href="part3.html">- Part 3</a>
                      <a href="part4.html">- Part 4</a>
                    </div>
                  </div>
                  
                    </div>
                </section>
            </section>
        `;
    }
}

customElements.define('my-menu', Menu);
