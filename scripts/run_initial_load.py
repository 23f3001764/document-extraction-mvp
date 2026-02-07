print("🚀 Starting initial data load...")

from scripts.process_constitution_variant_b import main as load_constitution
from scripts.process_all_pdfs import main as load_pdfs

load_constitution()
load_pdfs()

print("✅ Initial data load completed")