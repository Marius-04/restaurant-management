"""
LABORATORUL 5 - Flyweight, Decorator, Bridge & Proxy
Restaurant Management System
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional

# ============================================================================
# FLYWEIGHT - Gestionare Caractere
# ============================================================================

class Character:
    def __init__(self, char):
        self.char = char

class CharacterFactory:
    _pool: Dict[str, Character] = {}
    
    @staticmethod
    def get_character(char):
        if char not in CharacterFactory._pool:
            print(f"   ✨ Caracter nou: '{char}'")
            CharacterFactory._pool[char] = Character(char)
        else:
            print(f"   ♻️ Reutilizat: '{char}'")
        return CharacterFactory._pool[char]

# ============================================================================
# DECORATOR - Extindere Notificări
# ============================================================================

class Notification(ABC):
    @abstractmethod
    def send(self, msg): pass

class EmailNotification(Notification):
    def send(self, msg): return f"📧 Email: {msg}"

class NotificationDecorator(Notification):
    def __init__(self, notif):
        self.notif = notif
    
    def send(self, msg):
        return self.notif.send(msg)

class SMSDecorator(NotificationDecorator):
    def send(self, msg):
        base = self.notif.send(msg)
        return base + f" + 📱 SMS: {msg}"

class PushDecorator(NotificationDecorator):
    def send(self, msg):
        base = self.notif.send(msg)
        return base + f" + 🔔 Push: {msg}"

# ============================================================================
# BRIDGE - Separare Abstractie de Implementare
# ============================================================================

class DeviceImplementer(ABC):
    @abstractmethod
    def render(self): pass

class PhoneDevice(DeviceImplementer):
    def render(self): return "📱 Phone UI"

class TabletDevice(DeviceImplementer):
    def render(self): return "📱 Tablet UI"

class RemoteControl(ABC):
    def __init__(self, device):
        self.device = device
    
    @abstractmethod
    def show_menu(self): pass

class SimpleRemote(RemoteControl):
    def show_menu(self):
        return f"Menu pe {self.device.render()}"

# ============================================================================
# PROXY - Control Acces
# ============================================================================

class RealMenu:
    def __init__(self):
        print("   ⏳ Se încarcă meniu...")
        self.items = ["Paste", "Pizza", "Salata"]
        print("   ✅ Meniu încărcat\n")
    
    def get_items(self):
        return self.items

class MenuProxy:
    def __init__(self):
        self._real_menu: Optional[RealMenu] = None
    
    def get_items(self):
        if self._real_menu is None:
            print("   🔐 Proxy: Se creează meniu real")
            self._real_menu = RealMenu()
        else:
            print("   🔐 Proxy: Din cache\n")
        return self._real_menu.get_items()

# ============================================================================
# DEMONSTRAȚIE
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("LAB 5 - FLYWEIGHT, DECORATOR, BRIDGE & PROXY")
    print("="*70)
    
    # Flyweight
    print("\n✅ FLYWEIGHT:\n")
    
    text = "PIZZA"
    for char in text:
        CharacterFactory.get_character(char)
    
    text2 = "PIZZA"  # Reutilizează
    for char in text2:
        CharacterFactory.get_character(char)
    
    print()
    
    # Decorator
    print("✅ DECORATOR:\n")
    
    email = EmailNotification()
    email_sms = SMSDecorator(email)
    email_sms_push = PushDecorator(email_sms)
    
    print(f"  {email_sms_push.send('Comanda este gata')}\n")
    
    # Bridge
    print("✅ BRIDGE:\n")
    
    phone = SimpleRemote(PhoneDevice())
    tablet = SimpleRemote(TabletDevice())
    
    print(f"  {phone.show_menu()}")
    print(f"  {tablet.show_menu()}\n")
    
    # Proxy
    print("✅ PROXY:\n")
    
    menu_proxy = MenuProxy()
    print(f"  Items: {menu_proxy.get_items()}")
    print(f"  Items: {menu_proxy.get_items()}")
    
    print("="*70)
    print("✅ LAB 5 - COMPLET")
    print("="*70 + "\n")
