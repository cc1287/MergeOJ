import ErrorHook,json,os

class File():
    def __init__(self,fileType:str=['json','plain']):
        if not fileType in ['json','plain']:
            raise NameError("fileType 值应在 ['json','plain'] 中，找到{}".format(fileType))
        self.type=fileType
        self.path=os.path.dirname(os.path.abspath(__file__))
    def read(self,path,absPath=False) -> dict:
        with open(("" if absPath else self.path)+path,'r',encoding='utf-8') as f:
            if self.type=='json':
                return json.load(f)
            else:
                return f.read()
    def save(self,path,file,absPath=False,fileType='w'):
        with open(("" if absPath else self.path)+path,fileType,encoding='utf-8') as f:
            if self.type=='json':
                json.dump(file,f)
            else:
                f.write(str(file))
            
if __name__=='__main__':
    File('json')