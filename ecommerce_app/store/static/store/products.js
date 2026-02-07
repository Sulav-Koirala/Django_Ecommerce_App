const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

function get_products(){
    fetch('api/products/')
    .then(res => {
        if (!res.ok) {
            throw new Error(`Error, Status: ${res.status}`);
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
                html += `<button class="update" data-id="${p.id}">Update Details</button>
                        <button class="delete" data-id="${p.id}">Delete Product</button>`}
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
    const container = document.getElementById("add-container");
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
        .then(res => {
            if (!res.ok){
                return res.json().then(err => { throw err });
            }
            return res.json();
        })
        .then(data => {
            alert("Product added Successfully");
            document.getElementById("name").value="";
            document.getElementById("price").value="";
            document.getElementById("quantity").value="";
            document.getElementById("add-container").style.display="none";
            get_products();
        })
        .catch(err => {
            alert("Failed");
            console.error(err)});
    });
}

document.getElementById("list").addEventListener("click", (e) => {
    if (e.target.classList.contains("update")) {
        const btn = e.target;
        const id=btn.dataset.id;
        const productDiv = btn.closest(".description");
        const name = productDiv.querySelector("p:nth-child(1)").textContent.replace("Name: ", "");
        const price = productDiv.querySelector("p:nth-child(2)").textContent.replace("Price: ","");
        const quantity = productDiv.querySelector("p:nth-child(3)").textContent.replace("Quantity: ","");

        document.getElementById("update-id").value = id;
        document.getElementById("update-name").value = name;
        document.getElementById("update-price").value = parseFloat(price);
        document.getElementById("update-quantity").value = parseInt(quantity);
        document.getElementById("update-container").style.display = "block";
    }
});

document.getElementById("update-submit").addEventListener("click", () => {
    const id = document.getElementById("update-id").value;
    const name = document.getElementById("update-name").value;
    const price = document.getElementById("update-price").value;
    const quantity = document.getElementById("update-quantity").value;

    fetch(`api/products/${id}/`,{
        method: "PATCH",
        headers: {
            "Content-Type" : "application/json",
            "X-CSRFToken" : csrftoken
        },
        body: JSON.stringify({name,price,quantity})
    })
    .then(res => {
        if (!res.ok){
            return res.json().then(err => { throw err});
        }
        return res.json();
    })
    .then(data => {
        alert("Product details updated!");
        document.getElementById("update-container").style.display="none";
        get_products();
    })
    .catch(err => {
        alert("Failed");
        console.error(err)});
});

document.getElementById("list").addEventListener("click", (e) => {
    if (e.target.classList.contains("delete")) {
        const id = e.target.dataset.id;
    
        if (!confirm("Are you sure you want to delete this product?")) return;

        fetch(`api/products/${id}/`, {
            method: "DELETE",
            headers: {
                "X-CSRFToken": csrftoken
            }
        })
        .then(res => {
            if (!res.ok) throw new Error ("Delete Failed");
            alert("Deleted successfully");
            get_products();
        })
        .catch(err => console.error(err));
    }
});