"""data loaders and other data interacting functions for interacting with the json file"""
import json
import os
class DataLoader:
    """Set of functions to help loading and unloading data"""
    dirname = os.path.dirname(__file__)
    resume_path = (dirname+"//resume.json")


    @classmethod
    def load(cls, resume_class: str):
        """Loads JSON file to a dict"""
        resume_dict = {}
        #Get work Experience
        with open(cls.resume_path,"r") as data_file:
            try:
                resume_list = json.load(data_file).get(resume_class)
            except Exception:
                print("Error")
                raise Exception("Whoops")
        for data in resume_list:
            resume_dict[data["name"]] = data
        return resume_dict

    # Simply updates the recipe on the dict, but does not *save* it
    # or write it to the disk
    @classmethod
    def update_resume(cls, resume_item: dict, updated_item: dict):
        """Update Resume"""
        for key, val in updated_item.items():
            resume_item[key] = val

    # Helper method to allow us to turn the dict that we made when loading
    # back into a list, to allow us to save it on the disk
    # exactly how it was
    @staticmethod
    def dict_to_list(resume_dict: dict):
        """Helper Method, dict -> List"""
        resume_list =[]
        for name in resume_dict.keys():
            resume_list.append(resume_dict[name])
        return resume_list
    # we use this to write to disk
    @classmethod
    def write(cls, write_dict: dict):
        """Write Dict to disk"""
        resume_list = cls.dict_to_list(write_dict)
        with open("comments.json", "a") as data_file:
            json.dump({"comment": resume_list}, data_file, indent=2)
            
    @classmethod
    def add_comment(cls,comment,com_dir = dirname):
         """Write comment to comment file"""
         with open(com_dir+"\\comments.txt","a") as comment_text_file:
            comment_text_file.writelines(comment)
            comment_text_file.close()
            