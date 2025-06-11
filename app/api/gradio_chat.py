import gradio as gr
import shutil
import os
import uuid

from app.core.mq import publish_to_rabbitmq
from app.core.config import settings
from app.core import logger_utils
from app.pipeline.feature_pipeline.models.raw import DocumentRawModel

from pathlib import Path
ROOT_DIR = str(Path(__file__).parent.parent.parent.parent)
UPLOAD_FOLDER = os.path.join(ROOT_DIR, "uploads")

from docling.document_converter import DocumentConverter
from markitdown import MarkItDown


logger = logger_utils.get_logger(__name__)


def upload_files(files: list):

    if not os.path.isdir(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    shutil.copy(files[0], UPLOAD_FOLDER)

    gr.Info("开始文件解析")

    converter = DocumentConverter()
    doc = converter.convert(files[0]).document

    print(doc.export_to_markdown())

def process_uploaded_file(files: list, dir_files: list, file_name: str):
    """
    处理上传的文件，支持单个文件上传和目录上传两种方式。
    
    参数:
        files (list): 单个文件上传列表
        dir_files (list): 目录上传文件列表
        file_name (str): 上传的文件名
    
    返回:
        tuple: (状态消息, 文件名, 文件名)
    """
    try:
        # 过滤掉None值和空列表
        files = [f for f in files if f] if files else []
        dir_files = [f for f in dir_files if f] if dir_files else []
        
        # 合并所有文件
        files_list = files + dir_files
        
        if not files_list:
            return "未选择任何文件", "", ""
            
        doc_count = len(files_list)
        logger.info(f"共收到{doc_count}个文件，文件名：{files_list}")

        md = MarkItDown(enable_plugins=False)

        processed_count = 0
        for file in files_list:
            try:
                result = md.convert(file)
                data = DocumentRawModel(
                    knowledge_id="default",
                    doc_id="222",
                    path=file,
                    filename=file,
                    content=result.text_content,
                    type="documents",
                    entry_id=str(uuid.uuid4()),
                ).model_dump_json()
                publish_to_rabbitmq(queue_name='test_files', data=data)
                logger.info(f"成功处理并发送文件：{file}")
                processed_count += 1
            except Exception as e:
                logger.error(f"处理文件 {file} 时出错: {str(e)}")
                continue

        if processed_count == 0:
            return "文件处理失败，请检查文件格式是否正确", "", ""
            
        return f"成功处理 {processed_count}/{doc_count} 个文件", file_name, file_name

    except Exception as e:
        logger.error(f"处理上传文件时发生错误: {str(e)}")
        return f"处理文件时发生错误: {str(e)}", "", ""



def process_query():

    #return
    pass



with gr.Blocks(title="推理问答知识库") as demo:
    gr.Markdown("""
    # 推理问答系统
        支持多文件上传，大文档上传
        支持多文件夹上传，大文件夹上传
    """)

    with gr.Row():
        with gr.Column():

            files_input = gr.File(
                label="上传文档",
                file_types=[".txt", ".docx", ".pdf", ".csv", ".json"],
                type="filepath",
                file_count="multiple"
            )
            dir_input = gr.File(
                label="上传文件夹",
                file_types=[".txt", ".docx", ".pdf", ".csv", ".json"],
                type="filepath",
                file_count="directory"
            )

            file_name = gr.Textbox(label="文件名", visible=False)
            upload_button = gr.Button("加载文档到知识库")

            upload_output = gr.Textbox(label="上传状态", interactive=False)

            # 问题输入
            question_input = gr.Textbox(
                label="您的问题",
                placeholder="在此输入您的问题...",
                lines=3
            )
            show_reasoning = gr.Checkbox(
                label="显示推理过程",
                value=False
            )
            use_background = gr.Checkbox(
                label="使用背景调查",
                value=True
            )
            submit_btn = gr.Button("获取答案")

        with gr.Column():
            answer_output = gr.Textbox(
                label="答案",
                lines=10,
                interactive=False
            )


    # 处理文件上传
    def on_file_select(file):
        """处理文件选择"""
        if file is None:
            return "未选择文件", ""

        print(f"已选择文件: {type(file)}")
        if isinstance(file, str):  # filepath模式返回字符串路径
            logger.info(f"文件名: {os.path.basename(file)}, 路径:{os.path.splitext(file)[1]}")

            return os.path.basename(file), os.path.splitext(file)[1]
        elif hasattr(file, 'name'):
            logger.info(f"文件名: {file.name}, 路径:{os.path.splitext(file.name)[1]}")

            return file.name, os.path.splitext(file.name)[1]
        else:
            return "已选择文件（未知格式）", ".txt"


    files_input.change(
        fn=on_file_select,
        inputs=[files_input],
        outputs=[file_name, upload_output]
    )

    # 处理上传文件按钮点击
    upload_button.click(
        fn=process_uploaded_file,
        inputs=[files_input, dir_input, file_name],
        outputs=[upload_output, gr.State(), gr.State()]
    )


    # 处理提交按钮点击
    submit_btn.click(
        fn=process_query,
        inputs=[question_input, show_reasoning, use_background],
        outputs=answer_output
    )

    gr.Examples(
        examples=[
            ["这个文档的主题是什么?"],
            ["你能帮我总结出关键信息嘛?"],
            ["结论是什么?"]
        ],
        inputs=question_input
    )

# 启动应用
if __name__ == "__main__":

    # 启动应用
    demo.launch(server_name="0.0.0.0", share=True)
    #demo.launch(server_name="175.6.21.222", share=True)