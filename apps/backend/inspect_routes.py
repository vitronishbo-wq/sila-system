#!/usr/bin/env python3
"""Ferramenta para inspecionar rotas e saúde do sistema"""

import sys
import asyncio
from app.main import app

def print_routes():
    """Lista todas as rotas enregistadas"""
    routes = []
    
    for route in app.routes:
        methods = getattr(route, "methods", None)
        path = getattr(route, "path", None)
        name = getattr(route, "name", None)
        
        if methods and path:
            for method in sorted(methods):
                routes.append({
                    "method": method,
                    "path": path,
                    "name": name
                })
        elif path:
            routes.append({
                "method": "MOUNT",
                "path": path,
                "name": name
            })
    
    # Sort by path then method
    routes.sort(key=lambda x: (x["path"], x["method"]))
    
    print("\n" + "="*80)
    print("📍 ROTAS REGISTADAS - SILA SYSTEM")
    print("="*80)
    
    for route in routes:
        print(f"{route['method']:6} {route['path']:50} ({route['name'] or 'unnamed'})")
    
    print(f"\n✅ Total: {len(routes)} rotas\n")

if __name__ == "__main__":
    print_routes()
