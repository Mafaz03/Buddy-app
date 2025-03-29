import rumps
from pymongo import MongoClient
import uuid
from AppKit import NSPasteboard, NSArray

class DynamicStatusBarApp(rumps.App):
    def __init__(self):
        super(DynamicStatusBarApp, self).__init__("Loading...")
        # Connect to Mongo
        self.client = MongoClient("mongodb+srv://mohdmafaz200303:VeryHardPasswordToCrack@buddy.08mhtx4.mongodb.net/?retryWrites=true&w=majority&appName=buddy")
        self.db = self.client["Buddy"]

        self.pb = NSPasteboard.generalPasteboard()
    
        self.logo = "logo.png"
        self.texts = "..."
        self.collection_name = ""
        self.collection = None
        self.update_every_seconds = 10  # Default update interval in seconds
        self.timer = rumps.Timer(self.update_text, self.update_every_seconds)  # Calls update_text() every 10 seconds
        self.timer.start()
        self.menu = [
            rumps.MenuItem("Update Refresh Interval"),
            "5 seconds",
            "10 seconds",
            "15 seconds",
            "20 seconds",
            None,  # Separator
            rumps.MenuItem("Stop Updates"),
            rumps.MenuItem("Create new Community"),
            rumps.MenuItem("Join a Community"),
            rumps.MenuItem("Start Updates"),
        ]

    @rumps.clicked("5 seconds")
    def set_5_seconds(self, _):
        """Sets the update interval to 5 seconds."""
        self.interval = 5
        self.timer.interval = self.interval
        rumps.notification("Success", message="Update interval set to", subtitle="5 seconds")
    
    @rumps.clicked("10 seconds")
    def set_10_seconds(self, _):
        """Sets the update interval to 10 seconds."""
        self.interval = 10
        self.timer.interval = self.interval
        rumps.notification("Success", message="Update interval set to", subtitle="10 seconds")

    @rumps.clicked("15 seconds")
    def set_15_seconds(self, _):
        """Sets the update interval to 15 seconds."""
        self.interval = 15
        self.timer.interval = self.interval
        rumps.notification("Success", message="Update interval set to", subtitle="15 seconds")

    @rumps.clicked("20 seconds")
    def set_20_seconds(self, _):
        """Sets the update interval to 20 seconds."""
        self.interval = 20
        self.timer.interval = self.interval
        rumps.notification("Success", message="Update interval set to", subtitle="20 seconds")

    def update_every(self, _):
        self.update_every_seconds = rumps.Window("Enter update interval in seconds:", "Update Interval", default_text=str(self.update_every_seconds)).run()
        # print(self.update_every_seconds)
        # print(type(self.update_every_seconds))

    def update_text(self, _):
        """Updates the menu bar text every 10 seconds."""
        if self.collection is not None:  # Ensure that the collection is not None
            # Querying the collection to get the text
            text = self.collection.find_one({"_id": "Texts"})
            if text:
                self.title = text.get("text", "No Text Found")
            else:
                self.title = "No Text Found"
        else:
            self.title = "No collection selected"

    @rumps.clicked("Stop Updates")
    def stop_updates(self, _):
        """Stops text updates."""
        self.timer.stop()
        self.title = "Updates Stopped"

    @rumps.clicked("Create new Community")
    def create_community(self, _):
        """Creates a new Database Collection."""
        
        self.collection_name = uuid.uuid4().hex  # Generates a new collection name using uuid

        self.pb.clearContents()
        a = NSArray.arrayWithObject_(self.collection_name)
        self.pb.writeObjects_(a)
        
        self.collection = self.db[self.collection_name]  # Select the new collection
        # No need to create the collection manually; it gets created when you insert the first document
        self.collection.insert_one({"_id": "Texts", "text": "Welcome to your community!"})
        rumps.notification("Success", "Created new collection:", self.collection_name)

    @rumps.clicked("Join a Community")
    def join_community(self, _):
        """Allows user to input a collection name to join."""
        window = rumps.Window("Enter collection name:", "Join Community")
        window.add_button("Join")
        response = window.run()

        if response.clicked == 1:  # User clicked "Join"
            self.collection_name = response.text.strip()  # Get the collection name from the input
            # print(self.collection_name)
            if self.collection_name in self.db.list_collection_names():
                self.collection = self.db[self.collection_name]
                rumps.notification("Success", message="Joined collection", subtitle="Join Community")
            else:
                rumps.notification("Error", message="Collection not found", subtitle="Join Community")
        else:
            rumps.notification("Error", message="You canceled the join operation.", subtitle="Join Community")
        
    @rumps.clicked("Update Text")
    def update_text_manually(self, _):
        """Updates the text manually."""
        if self.collection is not None:
            text = self.collection.find_one({"_id": "Texts"})
            if text:
                new_text = rumps.Window("Enter new text:", "Update Text", default_text=text.get("text")).run()
                if new_text.clicked:
                    self.collection.update_one({"_id": "Texts"}, {"$set": {"text": new_text.text}})
                    rumps.notification("Success", message="Text updated", subtitle=new_text.text)
            else:
                rumps.notification("Error", message="No Text Found")
        else:
            rumps.notification("Error", message="No collection selected")

    @rumps.clicked("Start Updates")
    def start_updates(self, _):
        """Restarts text updates."""
        if not self.timer.is_running():
            self.timer.start()

if __name__ == "__main__":
    DynamicStatusBarApp().run()