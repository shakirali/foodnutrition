# Obsolete Code, Files, and Comments Report

## Files to Remove

### 1. Empty `presentation/` Directory
- **Location**: `/presentation/`
- **Reason**: Empty directory with no files
- **Action**: Remove the directory

### 2. `RAG_IMPLEMENTATION.md`
- **Location**: Root directory
- **Reason**: Implementation guide that may be redundant with README.md. The README already covers RAG setup and usage comprehensively.
- **Action**: Review if still needed, otherwise remove

## Obsolete Comments

### 1. Production CORS Comment
- **File**: `web/api.py` (line 54)
- **Current**: `allow_origins=["*"],  # In production, specify actual origins`
- **Action**: Either implement proper origin restriction or remove the comment if it's not actionable

### 2. Placeholder Profile Endpoint
- **File**: `web/api.py` (lines 127-128)
- **Current**: 
  ```python
  """Update user profile (placeholder for future implementation)."""
  # Profile storage will be implemented in a future update
  ```
- **Action**: Either implement the feature or remove the endpoint if not needed

### 3. Obsolete Main Block in api.py
- **File**: `web/api.py` (lines 141-143)
- **Current**:
  ```python
  if __name__ == "__main__":
      import uvicorn
      uvicorn.run(app, host="0.0.0.0", port=8000)
  ```
- **Reason**: Redundant since `web/run_server.py` handles server startup
- **Action**: Remove this block

## Code That Could Be Improved

### 1. Unused UserProfile Model
- **File**: `web/api.py` (lines 71-75)
- **Issue**: `UserProfile` model is defined but only used in a placeholder endpoint
- **Action**: Either implement profile storage or remove if not needed

### 2. Session ID Implementation
- **File**: `web/api.py` (line 115)
- **Current**: `session_id = message.session_id or "session_1"`
- **Issue**: Simple hardcoded session ID, not a real session management system
- **Action**: Either implement proper session management or document this as a limitation

## Documentation Comments (Keep - These are useful)

### 1. ChromaDB Metadata Comment
- **File**: `data/process_usda_data.py` (lines 69-70)
- **Status**: ✅ Keep - This is important documentation explaining why full_data isn't stored

### 2. Path Addition Comments
- **Files**: `web/api.py` (line 12), `web/run_server.py` (line 5), `scripts/setup_rag.py` (line 5)
- **Status**: ✅ Keep - These explain why sys.path is modified

## Summary

**Files to Remove:**
1. `presentation/` directory (empty)
2. `RAG_IMPLEMENTATION.md` (if redundant with README)

**Code/Comments to Remove:**
1. `web/api.py` lines 141-143 (obsolete main block)
2. `web/api.py` line 54 comment (or implement proper CORS)
3. `web/api.py` lines 125-129 (placeholder endpoint - either implement or remove)

**Code to Review:**
1. `UserProfile` model usage in `web/api.py`
2. Session ID implementation in `web/api.py`

