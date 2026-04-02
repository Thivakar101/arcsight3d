using UnityEngine;
using System.IO;

public class SceneBootstrap : MonoBehaviour
{
    public string modelPathToLoad;
    
    void Start()
    {
        // Read path from command line arguments if launched from desktop client
        string[] args = System.Environment.GetCommandLineArgs();
        for (int i = 0; i < args.Length; i++)
        {
            if (args[i] == "--load-model" && i + 1 < args.Length)
            {
                modelPathToLoad = args[i + 1];
            }
        }

        if (!string.IsNullOrEmpty(modelPathToLoad) && File.Exists(modelPathToLoad))
        {
            var loader = gameObject.AddComponent<RuntimeModelLoader>();
            loader.LoadModel(modelPathToLoad);
        }
        else
        {
            Debug.LogError("No valid model path provided.");
        }
    }
}
