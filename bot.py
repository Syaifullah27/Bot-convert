import os
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Fungsi untuk mengonversi TXT ke VCF
def convert_to_vcf(file_path, output_path):
    with open(file_path, 'r') as txt_file:
        lines = txt_file.readlines()

    with open(output_path, 'w') as vcf_file:
        for line in lines:
            line = line.strip()
            if line:  # Pastikan baris tidak kosong
                name, phone = line.split(",")  # Misalnya file txt berformat: Nama,Nomor
                vcf_file.write("BEGIN:VCARD\n")
                vcf_file.write("VERSION:3.0\n")
                vcf_file.write(f"FN:{name}\n")
                vcf_file.write(f"TEL:{phone}\n")
                vcf_file.write("END:VCARD\n\n")

# Handler untuk perintah /start
async def start(update: Update, context):
    await update.message.reply_text('Halo, kirimkan file TXT yang ingin kamu konversi ke VCF, Master!')

# Handler untuk file yang diunggah
async def handle_document(update: Update, context):
    document = update.message.document
    file = await document.get_file()

    # Mengunduh file
    file_path = os.path.join('downloads', document.file_name)
    await file.download_to_drive(file_path)

    # Buat nama file output VCF
    output_vcf_path = file_path.replace('.txt', '.vcf')

    # Mengonversi file TXT ke VCF
    convert_to_vcf(file_path, output_vcf_path)

    # Mengirimkan file VCF
    with open(output_vcf_path, 'rb') as vcf_file:
        await update.message.reply_document(document=InputFile(vcf_file, filename=os.path.basename(output_vcf_path)))

    # Hapus file setelah dikirim
    os.remove(file_path)
    os.remove(output_vcf_path)

# Fungsi utama untuk menjalankan bot
async def main():
    application = ApplicationBuilder().token('7450660825:AAGUEPm6Lo2HvqBnjlNy4gVUulwRzV1dfXc').build()

    # Inisialisasi aplikasi
    await application.initialize()

    # Tambahkan handler
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.TEXT, handle_document))

    # Mulai bot
    await application.start()

    # Tetap idle untuk menunggu perintah
    await application.updater.start_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
