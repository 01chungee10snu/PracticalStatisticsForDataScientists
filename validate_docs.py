from docs.docs_index import book_structure
import os


def validate_structure():
    missing = []
    for level, sections in book_structure.items():
        for sec in sections:
            path = os.path.join('docs', sec['file'])
            if not os.path.exists(path):
                missing.append(path)
    return missing


if __name__ == '__main__':
    missing = validate_structure()
    if missing:
        print('누락된 파일:', missing)
    else:
        print('모든 문서가 존재합니다.')
