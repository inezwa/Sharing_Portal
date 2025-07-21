class MaterialSearch {
    constructor() {
        this.form = document.getElementById('search-form');
        this.resultsContainer = document.getElementById('results-container');
        this.paginationContainer = document.getElementById('pagination-container');
        this.pageSize = 10;
        this.currentPage = 1;
        
        this.initEvents();
        this.loadResults();
    }
    
    initEvents() {
        // Form submission
        this.form.addEventListener('submit', e => {
            e.preventDefault();
            this.currentPage = 1;
            this.loadResults();
        });
        
        // Input changes (with debounce)
        this.form.querySelectorAll('input, select').forEach(el => {
            el.addEventListener('input', this.debounce(() => {
                this.currentPage = 1;
                this.loadResults();
            }, 300));
        });
    }
    
    debounce(func, wait) {
        let timeout;
        return () => {
            clearTimeout(timeout);
            timeout = setTimeout(func, wait);
        };
    }
    
    async loadResults() {
        try {
            this.showLoading();
            
            const params = new URLSearchParams(new FormData(this.form));
            params.append('page', this.currentPage);
            params.append('page_size', this.pageSize);
            
            const response = await fetch(`/api/materials/?${params}`);
            const data = await response.json();
            
            this.renderResults(data);
            this.renderPagination(data);
            
        } catch (error) {
            this.showError(error);
        }
    }
    
    renderResults(data) {
        this.resultsContainer.innerHTML = data.results.map(material => `
            <div class="material-card">
                <h3>${material.title}</h3>
                <div class="meta">
                    <span>${material.category_name}</span>
                    <span>${new Date(material.upload_date).toLocaleDateString()}</span>
                </div>
                <p>${material.description.substring(0, 100)}...</p>
                <a href="/material/${material.id}/">View Details</a>
            </div>
        `).join('');
    }
    
    renderPagination(data) {
        const totalPages = Math.ceil(data.total / data.page_size);
        
        this.paginationContainer.innerHTML = `
            <div class="pagination">
                ${this.currentPage > 1 ? 
                    `<button onclick="search.prevPage()">Previous</button>` : ''}
                
                <span>Page ${this.currentPage} of ${totalPages}</span>
                
                ${this.currentPage < totalPages ? 
                    `<button onclick="search.nextPage()">Next</button>` : ''}
            </div>
        `;
    }
    
    nextPage() {
        this.currentPage++;
        this.loadResults();
        window.scrollTo(0, 0);
    }
    
    prevPage() {
        this.currentPage--;
        this.loadResults();
        window.scrollTo(0, 0);
    }
    
    showLoading() {
        this.resultsContainer.innerHTML = `
            <div class="loading">
                <div class="spinner"></div>
                Loading materials...
            </div>
        `;
    }
    
    showError(error) {
        this.resultsContainer.innerHTML = `
            <div class="error">
                Error loading results: ${error.message}
            </div>
        `;
    }
}

// Initialize
const search = new MaterialSearch();