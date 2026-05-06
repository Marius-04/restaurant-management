"""12. VISITOR
Aceeasi structura de comanda exportata in formate diferite (JSON/CSV/XML).
"""
import json

class JSONExportVisitor:
    def visit(self, order_dict): return json.dumps(order_dict, ensure_ascii=False, indent=2)

class CSVExportVisitor:
    def visit(self, o):
        head = "id,total,status,payment,address"
        row = f'{o.get("id","")},{o["total"]},{o["status"]},{o["payment_method"]},"{o.get("delivery_address","")}"'
        return head + "\n" + row

class XMLExportVisitor:
    def visit(self, o):
        return ("<order>"
                f"<id>{o.get('id','')}</id><total>{o['total']}</total>"
                f"<status>{o['status']}</status><payment>{o['payment_method']}</payment>"
                f"<address>{o.get('delivery_address','')}</address></order>")
