const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

function get_products(){
    fetch('api/products/')
    .then(res => {
        if (!res.ok) {
            throw new Error(`HTTP error! Status: ${res.status}`);
        }
        return res.json();
    })
    .then(data => {
        let html = '';
        data.forEach(p => {
            html += `
                <div class="description">
                    <p>Name: ${p.name}</p>
                    <p>Price: ${p.price}</p>
                    <p>Quantity: ${p.quantity}</p>`
            if (isAdminUser){  
                html += `<button id="update" data-id="${p.id}">Update</button>
                        <button id="delete" data-id="${p.id}">Delete</button>`}
            html += `<button>Add to Cart</button>
                    </div>`;
        });
        document.getElementById('list').innerHTML = html;
    })
    .catch(err => console.error('Fetch error:', err));
}

document.addEventListener("DOMContentLoaded", () => {
    get_products();
});

function add_product(){
    const container = document.getElementById("container");
    container.style.display = container.style.display === "none" ? "block" : "none";

    document.getElementById("submit").addEventListener("click", () => {
        const name = document.getElementById("name").value.trim();
        const price = parseFloat(document.getElementById("price").value);
        const quantity = parseInt(document.getElementById("quantity").value);

        fetch('api/products/', {
            method : "POST",
            headers: {
                "Content-Type" : "application/json",
                "X-CSRFToken" : csrftoken
            },
            body : JSON.stringify({name,price,quantity})
        })
        .then(res => res.json())
        .then(data => {
            alert("Product added Successfully");
            document.getElementById("name").value="";
            document.getElementById("price").value="";
            document.getElementById("quantity").value="";
            document.getElementById("container").style.display="none";
            get_products();
        })
        .catch(err => console.error(err));
    });
}

document.getElementById("update").addEventListener("click", () => {
    
})