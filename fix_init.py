import os

files = [
    "backend/__init__.py",
    "backend/routers/__init__.py",
    "backend/services/__init__.py",
    "backend/models/__init__.py",
    "backend/utils/__init__.py",
]

for f in files:
    os.makedirs(os.path.dirname(f), exist_ok=True)
    with open(f, "w", encoding="utf-8") as file:
        file.write("")
    print(f"✅ Fixed: {f}")

print("\nAll __init__.py files fixed!")