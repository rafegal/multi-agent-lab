from datetime import datetime
from typing import Dict, Any


def generate_order() -> Dict[str, Any]:
    """Ferramenta responsável para gerar uma ordem, depois é necessário incluir os produtos no order detail."""
    order_id = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    with open(
        "vitra_doc/order_log.txt", "a"
    ) as log_file:
        log_file.write(f"{datetime.now()}: Order {order_id} created.\n")
    return {"order_id": order_id, "message": f"Order {order_id} created successfully."}


def generate_order_detail(
    order_id: str, product_id: int, product_name: str, quantity: int, total_price: float
) -> Dict[str, Any]:
    """Inclui itens em uma ordem."""
    with open(
        "vitra_doc/order_detail_log.txt",
        "a",
    ) as log_file:
        log_file.write(
            f"{datetime.now()}: Order {order_id} detail added for product {product_id} - {product_name} with quantity {quantity} at price {total_price}\n"
        )
    return {
        "order_id": order_id,
        "message": f"Order detail added for product {product_id} - {product_name} with quantity {quantity} at price {total_price}",
    }


def generate_invoice(order_id: str) -> Dict[str, Any]:
    """Gera a fatura para a ordem."""
    invoice_number = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    with open(
        "vitra_doc/billing_log.txt",
        "a",
    ) as log_file:
        log_file.write(
            f"{datetime.now()}: Invoice {invoice_number} generated for order {order_id}\n"
        )
    invoice_number = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    return {
        "invoice_number": invoice_number,
        "message": f"Invoice {invoice_number} generated for order {order_id}",
    }


def update_stock(product: str, quantity: str, order_id: str) -> Dict[str, Any]:
    """Registrar a saída do estoque."""
    with open(
        "vitra_doc/stock_log.txt", "a"
    ) as log_file:
        log_file.write(
            f"{datetime.now()}: Stock updated for product {product} with quantity {quantity} for order {order_id}\n"
        )
    return {"message": f"Stock updated for {product} and quantity {quantity}"}
