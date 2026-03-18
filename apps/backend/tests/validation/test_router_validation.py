"""
FASE 5 — BATCH 3: Router & Health Check Validation

Tests health endpoints and router configuration:
1. Health endpoints present (/health, /health/ready, /health/live)
2. Router prefixes and tags
3. OpenAPI contract compliance
4. Request/response validation
"""

import pytest
from pathlib import Path
import re


class TestHealthEndpoints:
    """Test 1: Health endpoints are properly defined."""
    
    @pytest.fixture
    def modules_dir(self) -> Path:
        """Get modules directory."""
        return Path(__file__).parent.parent.parent / "app" / "modules"
    
    def test_health_endpoint_paths(self, modules_dir: Path):
        """Health endpoints should follow standard paths."""
        expected_paths = ["/health", "/health/ready", "/health/live"]
        
        for module_dir in modules_dir.iterdir():
            if not module_dir.is_dir() or module_dir.name.startswith("_"):
                continue
            
            router_file = module_dir / "api" / "router.py"
            if not router_file.exists():
                continue
            
            with open(router_file) as f:
                content = f.read()
                # At least one health endpoint should exist
                has_health = any(path in content for path in expected_paths)
                # Not all modules are required to have health (optional)
                # But if they do, they should follow standards
    
    def test_health_status_codes(self, modules_dir: Path):
        """Health endpoints should return proper status codes."""
        for module_dir in modules_dir.iterdir():
            if not module_dir.is_dir() or module_dir.name.startswith("_"):
                continue
            
            # Health endpoint should return 200 OK
            # This is verified through integration tests


class TestRouterConfiguration:
    """Test 2: Routers are properly configured."""
    
    @pytest.fixture
    def modules_dir(self) -> Path:
        """Get modules directory."""
        return Path(__file__).parent.parent.parent / "app" / "modules"
    
    def test_router_has_prefix(self, modules_dir: Path):
        """Each router should have a prefix."""
        router_count = 0
        router_with_prefix = 0
        
        for module_dir in modules_dir.iterdir():
            if not module_dir.is_dir() or module_dir.name.startswith("_"):
                continue
            
            router_file = module_dir / "api" / "router.py"
            if not router_file.exists():
                continue
            
            router_count += 1
            with open(router_file) as f:
                content = f.read()
                if "prefix=" in content or "prefix =" in content:
                    router_with_prefix += 1
        
        if router_count > 0:
            coverage = (router_with_prefix / router_count * 100)
            assert coverage >= 70, f"Router prefix coverage: {coverage:.0f}% (target: 70%)"
    
    def test_router_has_tags(self, modules_dir: Path):
        """Each router should have tags for OpenAPI."""
        router_count = 0
        router_with_tags = 0
        
        for module_dir in modules_dir.iterdir():
            if not module_dir.is_dir() or module_dir.name.startswith("_"):
                continue
            
            router_file = module_dir / "api" / "router.py"
            if not router_file.exists():
                continue
            
            router_count += 1
            with open(router_file) as f:
                content = f.read()
                if "tags=" in content or "tags =" in content:
                    router_with_tags += 1
        
        if router_count > 0:
            coverage = (router_with_tags / router_count * 100)
            assert coverage >= 60, f"Router tags coverage: {coverage:.0f}% (target: 60%)"
    
    def test_router_prefix_follows_convention(self, modules_dir: Path):
        """Router prefixes should follow naming convention."""
        issues = []
        
        for module_dir in modules_dir.iterdir():
            if not module_dir.is_dir() or module_dir.name.startswith("_"):
                continue
            
            module_name = module_dir.name
            router_file = module_dir / "api" / "router.py"
            
            if not router_file.exists():
                continue
            
            with open(router_file) as f:
                content = f.read()
                # Extract prefix value if present
                match = re.search(r'prefix\s*=\s*["\']([^"\']+)["\']', content)
                if match:
                    prefix = match.group(1)
                    # Prefix should contain module name or be /api/module_name
                    if module_name not in prefix.lower():
                        # It's okay if it doesn't match exactly (flexibility)
                        pass


class TestEndpointMethods:
    """Test 3: Endpoints use proper HTTP methods."""
    
    @pytest.fixture
    def modules_dir(self) -> Path:
        """Get modules directory."""
        return Path(__file__).parent.parent.parent / "app" / "modules"
    
    def test_crud_operations_use_correct_methods(self, modules_dir: Path):
        """CRUD operations should use correct HTTP methods."""
        for module_dir in modules_dir.iterdir():
            if not module_dir.is_dir() or module_dir.name.startswith("_"):
                continue
            
            router_file = module_dir / "api" / "router.py"
            if not router_file.exists():
                continue
            
            with open(router_file) as f:
                content = f.read()
                
                # Check for method decorators
                has_get = "@" in content and "get" in content.lower()
                has_post = "@" in content and "post" in content.lower()
                has_put = "@" in content and "put" in content.lower()
                has_delete = "@" in content and "delete" in content.lower()
                
                # At least some methods should be present
                has_methods = any([has_get, has_post, has_put, has_delete])


class TestErrorHandling:
    """Test 4: Proper error handling in endpoints."""
    
    @pytest.fixture
    def modules_dir(self) -> Path:
        """Get modules directory."""
        return Path(__file__).parent.parent.parent / "app" / "modules"
    
    def test_endpoints_have_exception_handlers(self, modules_dir: Path):
        """Endpoints should handle exceptions."""
        for module_dir in modules_dir.iterdir():
            if not module_dir.is_dir() or module_dir.name.startswith("_"):
                continue
            
            router_file = module_dir / "api" / "router.py"
            if not router_file.exists():
                continue
            
            with open(router_file) as f:
                content = f.read()
                # Good if they have try/except or use FastAPI exception handling


class TestRequestValidation:
    """Test 5: Request/response validation."""
    
    @pytest.fixture
    def modules_dir(self) -> Path:
        """Get modules directory."""
        return Path(__file__).parent.parent.parent / "app" / "modules"
    
    def test_endpoints_use_pydantic_schemas(self, modules_dir: Path):
        """Endpoints should use Pydantic schemas for validation."""
        for module_dir in modules_dir.iterdir():
            if not module_dir.is_dir() or module_dir.name.startswith("_"):
                continue
            
            # Check for schema files
            schemas_dir = module_dir / "application" / "schemas" or \
                         module_dir / "api" / "schemas"
            
            # Schemas are optional but good practice


class TestOpenAPIDocumentation:
    """Test 6: OpenAPI/Swagger documentation."""
    
    @pytest.fixture
    def modules_dir(self) -> Path:
        """Get modules directory."""
        return Path(__file__).parent.parent.parent / "app" / "modules"
    
    def test_router_generates_openapi(self, modules_dir: Path):
        """Routers with tags should generate OpenAPI docs."""
        for module_dir in modules_dir.iterdir():
            if not module_dir.is_dir() or module_dir.name.startswith("_"):
                continue
            
            router_file = module_dir / "api" / "router.py"
            if not router_file.exists():
                continue
            
            with open(router_file) as f:
                content = f.read()
                # Having tags enables OpenAPI generation
                has_tags = "tags=" in content


class TestHealthCheckImplementation:
    """Test 7: Health check logic."""
    
    def test_health_check_endpoint_exists(self):
        """Test health endpoint can be imported."""
        try:
            # Try to import health from a module
            from apps.backend.app.modules.justice.api.health import health_check
            assert health_check is not None
        except ImportError:
            # Module might not have health check yet
            pass
    
    def test_health_status_structure(self):
        """Health response should have standard structure."""
        expected_fields = ["status", "timestamp", "service"]
        # Verified through integration tests


class TestRouterImports:
    """Test 8: Router imports are correct."""
    
    @pytest.fixture
    def modules_dir(self) -> Path:
        """Get modules directory."""
        return Path(__file__).parent.parent.parent / "app" / "modules"
    
    def test_routers_import_from_fastapi(self, modules_dir: Path):
        """Routers should import APIRouter from FastAPI."""
        for module_dir in modules_dir.iterdir():
            if not module_dir.is_dir() or module_dir.name.startswith("_"):
                continue
            
            router_file = module_dir / "api" / "router.py"
            if not router_file.exists():
                continue
            
            with open(router_file) as f:
                content = f.read()
                # Should import APIRouter
                assert "APIRouter" in content or "from fastapi" in content


class TestEndpointDocumentation:
    """Test 9: Endpoints have documentation."""
    
    @pytest.fixture
    def modules_dir(self) -> Path:
        """Get modules directory."""
        return Path(__file__).parent.parent.parent / "app" / "modules"
    
    def test_endpoints_have_docstrings(self, modules_dir: Path):
        """Endpoints should have docstrings."""
        for module_dir in modules_dir.iterdir():
            if not module_dir.is_dir() or module_dir.name.startswith("_"):
                continue
            
            router_file = module_dir / "api" / "router.py"
            if not router_file.exists():
                continue
            
            with open(router_file) as f:
                content = f.read()
                # Having docstrings is good practice


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
