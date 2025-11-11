import os, uuid, pdfplumber, pandas as pd
from abc import ABC, abstractmethod

class FileProcessor(ABC):
    @abstractmethod
    def process(self, input_path: str, output_folder: str) -> str:
        pass

class PDFProcessor(FileProcessor):
    def process(self, input_path, output_folder):
        output_rows, headers = [], None
        with pdfplumber.open(input_path) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if not table: continue
                for row in table:
                    if not row or 'Page' in row[0] or 'End of Report' in row[0]: continue
                    row = [cell.replace('\n','').strip() if cell else '' for cell in row]
                    if headers is None:
                        headers = row
                    else:
                        if row == headers: continue
                        output_rows.append(row)
        if not output_rows or headers is None:
            raise ValueError('No valid table found in PDF')
        max_cols = max(len(headers), *(len(r) for r in output_rows))
        headers += ['']*(max_cols-len(headers))
        data_rows = [r+['']*(max_cols-len(r)) for r in output_rows]
        df = pd.DataFrame(data_rows, columns=headers)
        filename = os.path.splitext(os.path.basename(input_path))[0]
        unique = uuid.uuid4().hex[:8]
        output_path = os.path.join(output_folder, f"{filename}_output_{unique}.xlsx")
        df.to_excel(output_path, index=False)
        return output_path

class CSVProcessor(FileProcessor):
    def process(self, input_path, output_folder):
        df = pd.read_csv(input_path)
        filename = os.path.splitext(os.path.basename(input_path))[0]
        unique = uuid.uuid4().hex[:8]
        output_path = os.path.join(output_folder, f"{filename}_output_{unique}.xlsx")
        df.to_excel(output_path, index=False)
        return output_path

class ExcelProcessor(FileProcessor):
    def process(self, input_path, output_folder):
        df = pd.read_excel(input_path)
        filename = os.path.splitext(os.path.basename(input_path))[0]
        unique = uuid.uuid4().hex[:8]
        output_path = os.path.join(output_folder, f"{filename}_output_{unique}.xlsx")
        df.to_excel(output_path, index=False)
        return output_path

class ProcessorFactory:
    _map = {'pdf': PDFProcessor, 'csv': CSVProcessor, 'xls': ExcelProcessor, 'xlsx': ExcelProcessor}
    @classmethod
    def get_processor(cls, filename):
        ext = filename.split('.')[-1].lower()
        if ext not in cls._map:
            raise ValueError(f"Unsupported file type: {ext}")
        return cls._map[ext]()
