from pathlib import Path


def discover(target: Path) -> dict[str, object]:
    poms = sorted(target.rglob("pom.xml"))
    sources = sorted(target.rglob("*.java"))
    tests = [p for p in sources if "src/test" in p.as_posix()]
    return {
        "pom_files": [str(p.relative_to(target)) for p in poms],
        "java_sources": len(sources),
        "java_tests": len(tests),
        "modules": max(1, len(poms)),
    }
